# ADR-0003: Celery + Redis do oceny zbiorów w tle
- **Status:** Propozycja
- **Kontekst:** Profilowanie i ocena jakości do 100 tys. wierszy trwają sekundy; nie mogą blokować żądania HTTP (NFR-03).
- **Decyzja:** Worker Celery z brokerem Redis; widok zwraca od razu status zadania.
- **Rozważane alternatywy:** Obliczenia w żądaniu HTTP (timeouty); własna kolejka w tabeli bazy (mniej usług, ale więcej własnego kodu).
- **Konsekwencje:** + standard w ekosystemie Django; − dwa dodatkowe kontenery (worker, Redis).
- **Autor i data:** 