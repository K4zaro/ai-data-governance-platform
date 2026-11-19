# ADR-0007: Pliki zbiorów w wolumenie Dockera (MinIO opcjonalnie w S6)
- **Status:** Propozycja
- **Kontekst:** Surowe pliki nie mogą trafiać do bazy ani być dostępne publicznie (NFR-01); w MVP chcemy mało usług.
- **Decyzja:** Pliki w wolumenie za warstwą storage (np. django-storages), dostępne tylko przez aplikację.
- **Rozważane alternatywy:** MinIO od pierwszego sprintu: dodatkowa usługa bez wartości w MVP.
- **Konsekwencje:** + prostota; − szyfrowanie w spoczynku przechodzi na S6.
- **Autor i data:** 