# ADR-0009: CI na GitHub Actions
- **Status:** Propozycja
- **Kontekst:** Kod jest na GitHubie; import do Bitbucketa jest wymagany dopiero na koniec semestru.
- **Decyzja:** Lint i testy na każdym PR w GitHub Actions; wynik jest warunkiem merge'a.
- **Rozważane alternatywy:** Bitbucket Pipelines: wymagałoby wcześniejszego importu repozytorium.
- **Konsekwencje:** + CI działa od razu; − po imporcie trzeba przenieść lub wyłączyć konfigurację.
- **Autor i data:** 