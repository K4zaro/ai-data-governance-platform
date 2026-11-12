# Git workflow

- Gałęzie: `main` (stabilna), `develop` (integracja), `feature/<KLUCZ>-<nr>-krotki-opis`, np. `feature/<KLUCZ>-12-upload-csv`.
- Zmiany tylko przez pull request do `develop`; minimum jedno review innej osoby; CI musi przejść. Autor PR nie zatwierdza własnego PR.
- Commity: krótkie, w trybie rozkazującym (np. „Dodaj endpoint rejestracji zbioru”), klucz ticketu w opisie.
- Sposób merge'a: **[DO USTALENIA]** (zwykły merge albo squash and merge). Po merge usuwamy gałąź.
- `main` aktualizujemy z `develop` na koniec sprintu.
- Nie używamy `git push --force` na wspólnych gałęziach (historia jest potrzebna do importu).
- Dokumentacja (`docs/`) leży w repozytorium obok kodu: `spec.md`, `plan.md`, `tasks.md`, `docs/adr/`.
- Sekretów nie commitujemy; `.env` jest poza repo, wzór w `.env.example`.
- Prowadzący jest dodany do repozytorium. Na koniec semestru repo jest importowane lub archiwizowane z pełną historią.

## Cykl pracy
```bash
git checkout develop && git pull
git checkout -b feature/<KLUCZ>-12-opis
# praca, potem:
git add <pliki> && git commit -m "<KLUCZ>-12: Dodaj ..."
git push -u origin feature/<KLUCZ>-12-opis
# pull request do develop, review, merge, usunięcie gałęzi
```