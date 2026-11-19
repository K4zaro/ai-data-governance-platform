# ADR-0002: Django z szablonami i HTMX (bez osobnego frontendu SPA)
- **Status:** Propozycja
- **Kontekst:** Zespół ma ograniczone doświadczenie z frontendem; analiza danych odbywa się w Pythonie.
- **Decyzja:** Django (ORM, migracje, auth, formularze, panel admina) z szablonami, HTMX, Bootstrap 5 i Chart.js. Całość w jednym języku.
- **Rozważane alternatywy:** FastAPI + React/TypeScript: osobny build i kontrakt API, więcej pracy przy małym zespole.
- **Konsekwencje:** + mało infrastruktury, szybki start; − brak REST API od początku (ewentualnie jako rozszerzenie S6), trudniejszy późniejszy podział prac na frontend i backend.
- **Uwaga:** Argument „nikt nie zna frontendu” trzeba potwierdzić w zespole.
- **Autor i data:** 