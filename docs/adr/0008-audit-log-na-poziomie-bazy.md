# ADR-0008: Audit log append-only wymuszony uprawnieniami bazy
- **Status:** Propozycja
- **Kontekst:** Niezmienność dziennika (NFR-02) nie może zależeć od poprawności kodu aplikacji.
- **Decyzja:** Dwa konta w bazie: właściciel schematu (migracje, uprawnienia DDL) i konto aplikacji z uprawnieniami INSERT i SELECT na tabeli `audit_log` (oraz nadanym dostępem do sekwencji). Test: UPDATE i DELETE kończą się błędem.
- **Rozważane alternatywy:** Blokada tylko w aplikacji: niewystarczająca.
- **Konsekwencje:** + realna niezmienność; − konfiguracja kont przy starcie kontenera i w CI.
- **Autor i data:** 