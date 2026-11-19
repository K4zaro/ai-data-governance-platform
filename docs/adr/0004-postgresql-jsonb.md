# ADR-0004: PostgreSQL 16 z JSONB
- **Status:** Propozycja
- **Kontekst:** Potrzebne silne więzy integralności (workflow, role) i elastyczne zapisy (wyniki per kolumna, odpowiedzi kwestionariuszy).
- **Decyzja:** Jedna baza PostgreSQL; JSONB na dane dynamiczne; lineage przez zapytania rekurencyjne (`WITH RECURSIVE`).
- **Rozważane alternatywy:** MongoDB + Neo4j + PostgreSQL: trzy silniki to zbędna złożoność.
- **Konsekwencje:** + jedna baza, transakcje; − zapytania rekurencyjne w Django wymagają surowego SQL (S6).
- **Autor i data:** 