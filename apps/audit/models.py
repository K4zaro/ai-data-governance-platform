from datetime import timezone as dt_timezone

from django.conf import settings
from django.db import models
from django.utils import timezone


class AuditLogImmutabilityError(PermissionError):
    """Raised when attempting to modify or delete an audit log entry."""


class AuditAction(models.TextChoices):
    DATASET_REGISTERED = "DATASET_REGISTERED", "Rejestracja zbioru"
    DATASET_VERSION_CREATED = "DATASET_VERSION_CREATED", "Nowa wersja zbioru"
    ASSIGNMENT_CHANGED = "ASSIGNMENT_CHANGED", "Zmiana przypisania"
    ROLE_CHANGED = "ROLE_CHANGED", "Zmiana roli"
    ACCESS_DENIED = "ACCESS_DENIED", "Odmowa dostępu (403)"


class AuditLogQuerySet(models.QuerySet):
    def update(self, **kwargs):
        raise AuditLogImmutabilityError(
            "Wpisy w audit_log są niezmienne — operacja update jest zabroniona."
        )

    def delete(self):
        raise AuditLogImmutabilityError(
            "Wpisy w audit_log są niezmienne — operacja delete jest zabroniona."
        )

    def _raw_delete(self, using):
        raise AuditLogImmutabilityError(
            "Wpisy w audit_log są niezmienne — operacja delete jest zabroniona."
        )

    def bulk_update(self, objs, fields, batch_size=None):
        raise AuditLogImmutabilityError(
            "Wpisy w audit_log są niezmienne — operacja bulk_update jest zabroniona."
        )

    def update_or_create(self, defaults=None, create_defaults=None, **kwargs):
        raise AuditLogImmutabilityError(
            "Wpisy w audit_log są niezmienne — operacja update_or_create jest zabroniona."
        )


class AuditLogManager(models.Manager):
    def get_queryset(self):
        return AuditLogQuerySet(self.model, using=self._db)


class AuditLog(models.Model):
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="audit_logs",
        verbose_name="Autor",
    )
    ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="Adres IP",
    )
    ts_utc = models.DateTimeField(
        default=timezone.now,
        editable=False,
        db_index=True,
        verbose_name="Czas (UTC)",
    )
    action = models.CharField(
        max_length=100,
        choices=AuditAction.choices,
        db_index=True,
        verbose_name="Akcja",
    )
    object_type = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name="Typ obiektu",
    )
    object_id = models.CharField(
        max_length=64,
        blank=True,
        default="",
        db_index=True,
        verbose_name="Identyfikator obiektu",
    )
    before = models.JSONField(
        null=True,
        blank=True,
        verbose_name="Stan przed",
    )
    after = models.JSONField(
        null=True,
        blank=True,
        verbose_name="Stan po",
    )

    objects = AuditLogManager()

    class Meta:
        db_table = "audit_log"
        base_manager_name = "objects"
        ordering = ["-ts_utc", "-id"]
        verbose_name = "Wpis dziennika audytu"
        verbose_name_plural = "Dziennik audytu"
        indexes = [
            models.Index(
                fields=["object_type", "object_id"],
                name="audit_log_object_idx",
            ),
        ]

    def __str__(self):
        actor_label = self.actor_id if self.actor_id is not None else "anonymous"
        return f"[{self.ts_utc.isoformat()}] {self.action} {self.object_type}:{self.object_id} (actor={actor_label})"

    def save(self, *args, **kwargs):
        if (
            not self._state.adding
            or kwargs.get("force_update")
            or kwargs.get("update_fields") is not None
        ):
            raise AuditLogImmutabilityError(
                "Wpisy w audit_log są niezmienne — nie można modyfikować istniejącego wpisu."
            )
        if self.pk is not None and type(self).objects.filter(pk=self.pk).exists():
            raise AuditLogImmutabilityError(
                "Wpisy w audit_log są niezmienne — wpis o podanym identyfikatorze już istnieje."
            )

        if self.ts_utc is None:
            self.ts_utc = timezone.now()
        elif timezone.is_naive(self.ts_utc):
            self.ts_utc = timezone.make_aware(self.ts_utc, dt_timezone.utc)
        else:
            self.ts_utc = self.ts_utc.astimezone(dt_timezone.utc)

        kwargs.setdefault("force_insert", True)
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise AuditLogImmutabilityError(
            "Wpisy w audit_log są niezmienne — nie można usuwać wpisów."
        )
