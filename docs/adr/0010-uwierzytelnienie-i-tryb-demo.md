# ADR-0010: Uwierzytelnianie Django, 6 grup i tryb demo
- **Status:** Propozycja
- **Kontekst:** Potrzebne role (AI_ENGINEER, DATA_OWNER, DATA_STEWARD, COMPLIANCE_OFFICER, DPO, ADMIN) i wygodne demo.
- **Decyzja:** Wbudowane auth Django, role jako grupy, uprawnienia sprawdzane po stronie serwera (mixiny i dekoratory). Tryb demo (`DEMO_MODE=true`) loguje na przygotowane konta ról i zapisuje przełączenie w audit logu; domyślnie wyłączony.
- **Rozważane alternatywy:** LDAP/SSO od początku (zależność od infrastruktury uczelni, do ustalenia z prowadzącym); przełącznik oparty o nagłówek (furtka do eskalacji uprawnień).
- **Konsekwencje:** + prostota; − brak SSO w MVP.
- **Autor i data:** 