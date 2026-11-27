from datetime import datetime, timedelta, timezone as dt_timezone
from uuid import uuid4

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db.models import ProtectedError
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.audit.admin import AuditLogAdmin
from apps.audit.models import AuditAction, AuditLog, AuditLogImmutabilityError
from apps.audit.services import AuditLogPIIError, get_client_ip, log_audit_event

User = get_user_model()


class AuditLogModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="auditor", password="StrongPassword123!")

    def test_table_and_column_names_match_data_model_spec(self):
        self.assertEqual(AuditLog._meta.db_table, "audit_log")
        self.assertEqual(AuditLog._meta.get_field("actor").column, "actor_id")
        field_names = {field.name for field in AuditLog._meta.get_fields()}
        self.assertTrue(
            {
                "id",
                "actor",
                "ip",
                "ts_utc",
                "action",
                "object_type",
                "object_id",
                "before",
                "after",
            }.issubset(field_names)
        )

    def test_create_audit_log_entry_with_utc_timestamp_and_json_payloads(self):
        dataset_uuid = str(uuid4())
        entry = AuditLog.objects.create(
            actor=self.user,
            ip="192.168.10.20",
            action=AuditAction.DATASET_REGISTERED,
            object_type="Dataset",
            object_id=dataset_uuid,
            before=None,
            after={"status": "DRAFT", "version_no": 1},
        )

        fetched = AuditLog.objects.get(pk=entry.pk)
        self.assertEqual(fetched.actor_id, self.user.pk)
        self.assertEqual(fetched.ip, "192.168.10.20")
        self.assertEqual(fetched.action, AuditAction.DATASET_REGISTERED)
        self.assertEqual(fetched.object_type, "Dataset")
        self.assertEqual(fetched.object_id, dataset_uuid)
        self.assertIsNone(fetched.before)
        self.assertEqual(fetched.after, {"status": "DRAFT", "version_no": 1})
        self.assertIsNotNone(fetched.ts_utc)
        self.assertTrue(timezone.is_aware(fetched.ts_utc))
        self.assertEqual(fetched.ts_utc.utcoffset(), timedelta(0))

    def test_non_utc_aware_timestamp_is_normalized_to_utc(self):
        warsaw_tz = dt_timezone(timedelta(hours=2))
        local_dt = datetime(2026, 11, 27, 14, 0, 0, tzinfo=warsaw_tz)
        entry = AuditLog.objects.create(
            actor=self.user,
            ts_utc=local_dt,
            action=AuditAction.ROLE_CHANGED,
            object_type="User",
            object_id=str(self.user.pk),
        )
        self.assertEqual(entry.ts_utc.utcoffset(), timedelta(0))
        self.assertEqual(entry.ts_utc.hour, 12)

    def test_cannot_modify_existing_entry_via_save(self):
        entry = AuditLog.objects.create(
            actor=self.user,
            ip="10.0.0.5",
            action=AuditAction.ROLE_CHANGED,
            object_type="User",
            object_id="42",
            before={"roles": ["AI_ENGINEER"]},
            after={"roles": ["AI_ENGINEER", "DATA_OWNER"]},
        )

        entry.action = AuditAction.ACCESS_DENIED
        with self.assertRaises(AuditLogImmutabilityError):
            entry.save()

        with self.assertRaises(AuditLogImmutabilityError):
            entry.save(update_fields=["action"])

        with self.assertRaises(AuditLogImmutabilityError):
            AuditLog(
                pk=entry.pk,
                actor=self.user,
                action=AuditAction.ACCESS_DENIED,
                object_type="User",
                object_id="42",
            ).save()

        refreshed = AuditLog.objects.get(pk=entry.pk)
        self.assertEqual(refreshed.action, AuditAction.ROLE_CHANGED)

    def test_cannot_delete_entry_via_instance_or_queryset(self):
        entry = AuditLog.objects.create(
            actor=self.user,
            action=AuditAction.ACCESS_DENIED,
            object_type="View",
            object_id="/catalog/upload/",
        )

        with self.assertRaises(AuditLogImmutabilityError):
            entry.delete()

        with self.assertRaises(AuditLogImmutabilityError):
            AuditLog.objects.filter(pk=entry.pk).delete()

        with self.assertRaises(AuditLogImmutabilityError):
            AuditLog.objects.all().delete()

        self.assertEqual(AuditLog.objects.filter(pk=entry.pk).count(), 1)

    def test_cannot_update_entries_via_queryset_methods(self):
        entry = AuditLog.objects.create(
            actor=self.user,
            action=AuditAction.ASSIGNMENT_CHANGED,
            object_type="DatasetAssignment",
            object_id="7",
            before={"owners": [1]},
            after={"owners": [1, 2]},
        )

        with self.assertRaises(AuditLogImmutabilityError):
            AuditLog.objects.filter(pk=entry.pk).update(action=AuditAction.ACCESS_DENIED)

        with self.assertRaises(AuditLogImmutabilityError):
            AuditLog.objects.update(object_type="Tampered")

        entry.action = AuditAction.ACCESS_DENIED
        with self.assertRaises(AuditLogImmutabilityError):
            AuditLog.objects.bulk_update([entry], ["action"])

        with self.assertRaises(AuditLogImmutabilityError):
            AuditLog.objects.update_or_create(
                pk=entry.pk,
                defaults={"action": AuditAction.ACCESS_DENIED},
            )

        refreshed = AuditLog.objects.get(pk=entry.pk)
        self.assertEqual(refreshed.action, AuditAction.ASSIGNMENT_CHANGED)

    def test_cannot_bypass_immutability_via_base_manager(self):
        entry = AuditLog.objects.create(
            actor=self.user,
            action=AuditAction.ROLE_CHANGED,
            object_type="User",
            object_id="99",
            before={"roles": []},
            after={"roles": ["ADMIN"]},
        )

        self.assertEqual(AuditLog._meta.base_manager_name, "objects")

        with self.assertRaises(AuditLogImmutabilityError):
            AuditLog._base_manager.filter(pk=entry.pk).update(action="HACKED")

        with self.assertRaises(AuditLogImmutabilityError):
            AuditLog._base_manager.update(object_type="HACKED")

        with self.assertRaises(AuditLogImmutabilityError):
            AuditLog._base_manager.filter(pk=entry.pk).delete()

        with self.assertRaises(AuditLogImmutabilityError):
            AuditLog._base_manager.all().delete()

        entry.action = AuditAction.ACCESS_DENIED
        with self.assertRaises(AuditLogImmutabilityError):
            AuditLog._base_manager.bulk_update([entry], ["action"])

        refreshed = AuditLog.objects.get(pk=entry.pk)
        self.assertEqual(refreshed.action, AuditAction.ROLE_CHANGED)
        self.assertEqual(AuditLog.objects.filter(pk=entry.pk).count(), 1)

    def test_referenced_actor_cannot_be_deleted_silently(self):
        AuditLog.objects.create(
            actor=self.user,
            action=AuditAction.DATASET_REGISTERED,
            object_type="Dataset",
            object_id=str(uuid4()),
        )
        with self.assertRaises(ProtectedError):
            self.user.delete()


class AuditLogServiceTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="owner_user", password="StrongPassword123!")

    def test_log_audit_event_records_sprint_2_events(self):
        dataset_id = uuid4()
        request = self.factory.post("/catalog/register/", REMOTE_ADDR="198.51.100.12")
        request.user = self.user

        events = [
            log_audit_event(
                action=AuditAction.DATASET_REGISTERED,
                object_type="Dataset",
                object_id=dataset_id,
                request=request,
                before=None,
                after={"status": "DRAFT", "version_no": 1, "tags": ["finance"]},
            ),
            log_audit_event(
                action=AuditAction.DATASET_VERSION_CREATED,
                object_type="DatasetVersion",
                object_id=101,
                request=request,
                before={"latest_version_no": 1},
                after={"latest_version_no": 2, "processing_status": "PENDING"},
            ),
            log_audit_event(
                action=AuditAction.ASSIGNMENT_CHANGED,
                object_type="DatasetAssignment",
                object_id=dataset_id,
                request=request,
                before={"owners": [self.user.pk], "stewards": []},
                after={"owners": [self.user.pk], "stewards": [2]},
            ),
            log_audit_event(
                action=AuditAction.ROLE_CHANGED,
                object_type="User",
                object_id=self.user.pk,
                request=request,
                before={"roles": ["AI_ENGINEER"]},
                after={"roles": ["AI_ENGINEER", "DATA_OWNER"]},
            ),
            log_audit_event(
                action=AuditAction.ACCESS_DENIED,
                object_type="Endpoint",
                object_id="/catalog/register/",
                request=request,
                before=None,
                after={"status_code": 403, "required_roles": ["DATA_OWNER"]},
            ),
        ]

        self.assertEqual(len(events), 5)
        self.assertEqual(AuditLog.objects.count(), 5)
        self.assertEqual(events[0].actor, self.user)
        self.assertEqual(events[0].ip, "198.51.100.12")
        self.assertEqual(events[0].object_id, str(dataset_id))

    def test_log_audit_event_handles_anonymous_request(self):
        request = self.factory.get("/catalog/register/", REMOTE_ADDR="2001:db8::1")
        request.user = AnonymousUser()

        entry = log_audit_event(
            action=AuditAction.ACCESS_DENIED,
            object_type="Endpoint",
            object_id="/catalog/register/",
            request=request,
            after={"status_code": 403},
        )
        self.assertIsNone(entry.actor)
        self.assertEqual(entry.ip, "2001:db8::1")

    @override_settings(AUDIT_TRUST_X_FORWARDED_FOR=False, AUDIT_TRUSTED_PROXIES=[])
    def test_ip_ignores_x_forwarded_for_by_default(self):
        request = self.factory.get(
            "/",
            REMOTE_ADDR="192.0.2.10",
            HTTP_X_FORWARDED_FOR="203.0.113.99, 10.0.0.1",
        )
        self.assertEqual(get_client_ip(request), "192.0.2.10")

    @override_settings(AUDIT_TRUST_X_FORWARDED_FOR=True, AUDIT_TRUSTED_PROXIES=[])
    def test_ip_ignores_x_forwarded_for_when_trusted_proxies_empty(self):
        request = self.factory.get(
            "/",
            REMOTE_ADDR="192.0.2.25",
            HTTP_X_FORWARDED_FOR="1.2.3.4, 10.0.0.2",
        )
        self.assertEqual(get_client_ip(request), "192.0.2.25")

    @override_settings(
        AUDIT_TRUST_X_FORWARDED_FOR=True,
        AUDIT_TRUSTED_PROXIES=["10.0.0.0/8"],
    )
    def test_ip_falls_back_to_remote_addr_when_x_forwarded_for_is_invalid(self):
        request = self.factory.get(
            "/",
            REMOTE_ADDR="10.0.0.15",
            HTTP_X_FORWARDED_FOR="not-an-ip, spoofed",
        )
        self.assertEqual(get_client_ip(request), "10.0.0.15")

    @override_settings(
        AUDIT_TRUST_X_FORWARDED_FOR=True,
        AUDIT_TRUSTED_PROXIES=["10.0.0.0/8", "127.0.0.1"],
    )
    def test_ip_respects_trusted_proxies_list(self):
        untrusted_request = self.factory.get(
            "/",
            REMOTE_ADDR="198.51.100.7",
            HTTP_X_FORWARDED_FOR="203.0.113.88",
        )
        self.assertEqual(get_client_ip(untrusted_request), "198.51.100.7")

        trusted_request = self.factory.get(
            "/",
            REMOTE_ADDR="10.1.2.3",
            HTTP_X_FORWARDED_FOR="1.2.3.4, 203.0.113.77, 10.0.0.5",
        )
        self.assertEqual(get_client_ip(trusted_request), "203.0.113.77")

    def test_ip_returns_none_without_request(self):
        self.assertIsNone(get_client_ip(None))

    def test_pii_keys_and_values_are_rejected_in_before_and_after(self):
        with self.assertRaises(AuditLogPIIError):
            log_audit_event(
                action=AuditAction.ROLE_CHANGED,
                object_type="User",
                object_id=self.user.pk,
                after={"email": "jan.kowalski@example.com"},
            )

        with self.assertRaises(AuditLogPIIError):
            log_audit_event(
                action=AuditAction.DATASET_REGISTERED,
                object_type="Dataset",
                object_id=str(uuid4()),
                before={"nested": {"pesel": "44051401359"}},
            )

        with self.assertRaises(AuditLogPIIError):
            log_audit_event(
                action=AuditAction.DATASET_REGISTERED,
                object_type="Dataset",
                object_id=str(uuid4()),
                after={"note": "Jan 44051401359"},
            )

        with self.assertRaises(AuditLogPIIError):
            log_audit_event(
                action=AuditAction.DATASET_REGISTERED,
                object_type="Dataset",
                object_id=str(uuid4()),
                after={"note": "contact user@example.org"},
            )

        with self.assertRaises(AuditLogPIIError):
            log_audit_event(
                action=AuditAction.DATASET_REGISTERED,
                object_type="Dataset",
                object_id=str(uuid4()),
                after={"note": "PL61109010140000071219812874"},
            )

        self.assertEqual(AuditLog.objects.count(), 0)

    def test_invalid_required_parameters_raise_value_error(self):
        with self.assertRaises(ValueError):
            log_audit_event(action="", object_type="Dataset")

        with self.assertRaises(ValueError):
            log_audit_event(action="TOTALLY_MADE_UP", object_type="Dataset")

        with self.assertRaises(ValueError):
            log_audit_event(action=AuditAction.DATASET_REGISTERED, object_type="")

        with self.assertRaises(ValueError):
            log_audit_event(
                action=AuditAction.DATASET_REGISTERED,
                object_type="Dataset",
                ip="invalid-ip",
            )

        self.assertEqual(AuditLog.objects.count(), 0)


class AuditLogAdminTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.superuser = User.objects.create_superuser(
            username="admin_user",
            email="admin@example.com",
            password="StrongAdminPassword123!",
        )
        self.entry = log_audit_event(
            action=AuditAction.ROLE_CHANGED,
            object_type="User",
            object_id=str(self.superuser.pk),
            actor=self.superuser,
            ip="127.0.0.1",
            before={"roles": []},
            after={"roles": ["ADMIN"]},
        )

    def test_admin_permissions_are_strictly_read_only(self):
        self.assertIn(AuditLog, admin.site._registry)
        model_admin = admin.site._registry[AuditLog]
        self.assertIsInstance(model_admin, AuditLogAdmin)

        request = self.factory.get("/admin/audit/auditlog/")
        request.user = self.superuser

        self.assertFalse(model_admin.has_add_permission(request))
        self.assertFalse(model_admin.has_change_permission(request, self.entry))
        self.assertFalse(model_admin.has_delete_permission(request, self.entry))
        self.assertTrue(model_admin.has_view_permission(request, self.entry))
        self.assertEqual(model_admin.get_actions(request), {})

    def test_admin_views_allow_read_and_forbid_add_or_delete(self):
        self.client.force_login(self.superuser)

        changelist_url = reverse("admin:audit_auditlog_changelist")
        detail_url = reverse("admin:audit_auditlog_change", args=[self.entry.pk])
        add_url = reverse("admin:audit_auditlog_add")
        delete_url = reverse("admin:audit_auditlog_delete", args=[self.entry.pk])

        self.assertEqual(self.client.get(changelist_url).status_code, 200)
        self.assertEqual(self.client.get(detail_url).status_code, 200)
        self.assertEqual(self.client.get(add_url).status_code, 403)
        self.assertEqual(self.client.post(delete_url).status_code, 403)
        self.assertEqual(AuditLog.objects.count(), 1)
