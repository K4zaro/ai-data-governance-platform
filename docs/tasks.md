# tasks.md: KROKI

**Status:** Propozycja v0.1. SP wyceniamy zespołowo (Planning Poker).

## Sprint 1: dokumentacja i fundamenty
Cel: Mamy uzgodniony zakres MVP, spójną specyfikację, architekturę i backlog na kolejne sprinty.

| Ticket | Kryteria akceptacji (skrót) | SP | Osoba |
|---|---|---|---|
| Confluence: struktura i szablony | Drzewo stron, szablony sprintu i ADR | | [ ] |
| Working Agreement i role | Zatwierdzone przez zespół | | [ ] |
| Product Vision & Scope | Zakres MVP/S6 potwierdzony | | [ ] |
| spec.md v0.2 | Przegląd w PR, rozbieżności rozstrzygnięte | | [ ] |
| PR-01 | Zsynchronizowany ze spec.md | | [ ] |
| ADR-y (0001-0010) | Autor i status przy każdym | | [ ] |
| Diagramy C4: kontekst i kontenery | W plan.md | | [ ] |
| Model danych (ER) | Zgodny ze spec.md, sekcja 8 | | [ ] |
| Backlog Jiry: epiki i historyjki sprintu 2 | Kryteria akceptacji, priorytety | | [ ] |
| *Opcjonalnie:* makiety, CI, DPIA (szablon), szkielet Django (`docker compose up`, `/health`) | Jeśli starczy czasu | | [ ] |

## Sprint 2: katalog i szkielet przetwarzania
US-101, US-102, US-104, zadanie Celery z profilem kolumn, audit log (US-501).
Rezultat na review: wgrany CSV pojawia się w katalogu z listą kolumn i typów.

## Sprint 3: silnik jakości
US-103, US-201, US-202, US-203.
Rezultat: dashboard jakości zbioru demo; kolumny PII oznaczone. Sprint przeładowany: ocenić na planningu.

## Sprint 4: workflow i compliance
US-301, US-302, US-303, US-401, US-402, US-404, US-405, US-503.
Rezultat: wniosek przechodzi 4 etapy; zwrot i odrzucenie działają. Sprint przeładowany: ocenić na planningu.

## Sprint 5: domknięcie semestru V
Seeder, tryb demo (US-003), testy, poprawki, dokumentacja, prezentacja.

## Semestr VI (S6): szkic
6: formaty Parquet/JSON, lineage (US-105). 7: monitoring jakości, trend, alerty, rekomendacje (US-204, US-205). 8: lista art. 10, bias, NER (US-305, US-304). 9: maskowanie, certyfikat PDF, szyfrowanie plików (US-306, US-502). 10: wersja końcowa, wdrożenie na serwerze uczelni, dokumentacja końcowa.