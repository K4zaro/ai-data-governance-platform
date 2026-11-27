from __future__ import annotations

import ipaddress
import re
from typing import Any
from uuid import UUID

from django.conf import settings
from django.http import HttpRequest

from apps.audit.models import AuditLog

FORBIDDEN_PII_KEYS = frozenset(
    {
        "pesel",
        "email",
        "e_mail",
        "phone",
        "phone_number",
        "telefon",
        "numer_telefonu",
        "iban",
        "bank_account",
        "account_number",
        "numer_konta",
        "password",
        "haslo",
        "secret",
        "token",
        "first_name",
        "last_name",
        "imie",
        "nazwisko",
        "full_name",
        "address",
        "adres",
        "street",
        "ulica",
        "birth_date",
        "data_urodzenia",
        "nip",
        "ssn",
        "raw_data",
        "raw_values",
        "sample_rows",
    }
)

_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_PESEL_CANDIDATE_RE = re.compile(r"(?<!\d)(\d{11})(?!\d)")
_PL_IBAN_RE = re.compile(r"\bPL\s?\d{2}(?:\s?\d{4}){6}\b", re.IGNORECASE)
_PESEL_WEIGHTS = (1, 3, 7, 9, 1, 3, 7, 9, 1, 3)


class AuditLogPIIError(ValueError):
    """Raised when audit log state payloads appear to contain PII values."""


def _is_valid_pesel(value: str) -> bool:
    if len(value) != 11 or not value.isdigit():
        return False
    checksum = sum(int(digit) * weight for digit, weight in zip(value[:10], _PESEL_WEIGHTS))
    control = (10 - (checksum % 10)) % 10
    return control == int(value[10])


def _normalize_key(key: str) -> str:
    return re.sub(r"[\s\-]+", "_", key.strip().lower())


def _validate_no_pii_payload(payload: Any, field_name: str, path: str = "") -> None:
    if payload is None:
        return

    if isinstance(payload, dict):
        for raw_key, value in payload.items():
            key_str = str(raw_key)
            current_path = f"{path}.{key_str}" if path else key_str
            if _normalize_key(key_str) in FORBIDDEN_PII_KEYS:
                raise AuditLogPIIError(
                    f"Pole '{field_name}' zawiera niedozwolony klucz PII/wrażliwy: '{current_path}'."
                )
            _validate_no_pii_payload(value, field_name, current_path)
    elif isinstance(payload, (list, tuple)):
        for index, item in enumerate(payload):
            current_path = f"{path}[{index}]" if path else f"[{index}]"
            _validate_no_pii_payload(item, field_name, current_path)
    elif isinstance(payload, str):
        location = f" w '{path}'" if path else ""
        if _EMAIL_RE.search(payload):
            raise AuditLogPIIError(
                f"Pole '{field_name}'{location} zawiera wartość przypominającą adres e-mail (PII)."
            )
        if _PL_IBAN_RE.search(payload):
            raise AuditLogPIIError(
                f"Pole '{field_name}'{location} zawiera wartość przypominającą numer IBAN (PII)."
            )
        for match in _PESEL_CANDIDATE_RE.finditer(payload):
            if _is_valid_pesel(match.group(1)):
                raise AuditLogPIIError(
                    f"Pole '{field_name}'{location} zawiera wartość przypominającą numer PESEL (PII)."
                )


def _parse_ip(raw_ip: str | None) -> str | None:
    if not raw_ip:
        return None
    candidate = raw_ip.strip()
    if not candidate:
        return None
    try:
        return str(ipaddress.ip_address(candidate))
    except ValueError:
        return None


def _is_trusted_proxy(ip_str: str | None, trusted_proxies: list[str] | tuple[str, ...]) -> bool:
    if not ip_str or not trusted_proxies:
        return False
    try:
        ip_obj = ipaddress.ip_address(ip_str)
    except ValueError:
        return False

    for entry in trusted_proxies:
        entry = entry.strip()
        if not entry:
            continue
        try:
            if "/" in entry:
                if ip_obj in ipaddress.ip_network(entry, strict=False):
                    return True
            else:
                if ip_obj == ipaddress.ip_address(entry):
                    return True
        except ValueError:
            continue
    return False


def get_client_ip(request: HttpRequest | None) -> str | None:
    """Extract client IP cautiously.

    Never trusts X-Forwarded-For unless AUDIT_TRUST_X_FORWARDED_FOR is explicitly enabled.
    When AUDIT_TRUSTED_PROXIES is also configured, only trusts X-Forwarded-For if REMOTE_ADDR
    belongs to a trusted proxy, and strips trusted proxy hops from right to left.
    """
    if request is None:
        return None

    remote_addr = _parse_ip(request.META.get("REMOTE_ADDR"))
    trust_xff = bool(getattr(settings, "AUDIT_TRUST_X_FORWARDED_FOR", False))
    if not trust_xff:
        return remote_addr

    trusted_proxies = list(getattr(settings, "AUDIT_TRUSTED_PROXIES", []))
    if trusted_proxies and not _is_trusted_proxy(remote_addr, trusted_proxies):
        return remote_addr

    xff_header = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if not xff_header:
        return remote_addr

    forwarded_ips = [_parse_ip(part) for part in xff_header.split(",")]
    valid_forwarded = [ip for ip in forwarded_ips if ip is not None]
    if not valid_forwarded:
        return remote_addr

    if trusted_proxies:
        for ip_candidate in reversed(valid_forwarded):
            if not _is_trusted_proxy(ip_candidate, trusted_proxies):
                return ip_candidate
        return valid_forwarded[0]

    return valid_forwarded[0]


def log_audit_event(
    *,
    action: str,
    object_type: str,
    object_id: str | int | UUID | None = "",
    actor: Any = None,
    request: HttpRequest | None = None,
    ip: str | None = None,
    before: dict[str, Any] | list[Any] | None = None,
    after: dict[str, Any] | list[Any] | None = None,
) -> AuditLog:
    """Single service entry point used by all modules to record an immutable audit event."""
    if not action or not str(action).strip():
        raise ValueError("Parametr 'action' jest wymagany.")
    if not object_type or not str(object_type).strip():
        raise ValueError("Parametr 'object_type' jest wymagany.")

    resolved_actor = actor
    if resolved_actor is None and request is not None:
        resolved_actor = getattr(request, "user", None)
    if resolved_actor is not None and not getattr(resolved_actor, "is_authenticated", True):
        resolved_actor = None

    if ip is not None:
        resolved_ip = _parse_ip(ip)
        if resolved_ip is None:
            raise ValueError(f"Niepoprawny adres IP: '{ip}'.")
    else:
        resolved_ip = get_client_ip(request)

    _validate_no_pii_payload(before, "before")
    _validate_no_pii_payload(after, "after")

    resolved_object_id = "" if object_id is None else str(object_id)

    return AuditLog.objects.create(
        actor=resolved_actor,
        ip=resolved_ip,
        action=str(action).strip(),
        object_type=str(object_type).strip(),
        object_id=resolved_object_id,
        before=before,
        after=after,
    )
