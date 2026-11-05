## STRONA 9: Git workflow **[propozycja]**
 
- Gałęzie: `main` (stabilna), `develop` (integracja), `feature/<id-ticketu>-krotki-opis`.
- Nazwa gałęzi zawiera klucz ticketu z Jiry (np. `feature/DGP-12-upload-csv`), co łączy kod z backlogiem.
- Zmiany tylko przez pull request do `develop`; minimum jedno review; CI musi przejść.
- Commity: krótkie, w trybie rozkazującym (np. „Dodaj endpoint rejestracji zbioru”); klucz ticketu w opisie.
- `main` aktualizujemy z `develop` na koniec sprintu.
- Dokumentacja (`docs/`) leży w repozytorium obok kodu: `spec.md`, `plan.md`, `tasks.md`, `docs/adr/`.
- Prowadzący jest dodany do repozytorium. Na koniec semestru repo jest importowane lub archiwizowane z pełną historią.
---
