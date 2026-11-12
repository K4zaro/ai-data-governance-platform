# Platforma Data Governance & AI Act Compliance
Platforma webowa do oceny jakości i zarządzania zgodnością zbiorów danych używanych w systemach AI.

## Zespół
| Osoba | Rola / obszar |
|---|---|
| [Kamil Osakowicz ] | [ ] |
| [Radek Kulesza ] | [ ] |
| [Michał Spaliński ] | [ ] |
| [Filip Kamiński ] | [ ] |
| [Konrad Zajczyk ] | [ ] |

## Linki
- Jira: [link]
- Confluence: [link]
- Teams: [kanał]

## Stos technologiczny
Python 3.12, Django 5.2 LTS, szablony + HTMX, Bootstrap 5, Chart.js, Celery + Redis, pandas, PostgreSQL 16, Docker Compose.

## Dokumentacja
- Specyfikacja (CO i DLACZEGO): docs/spec.md
- Plan (JAK): docs/plan.md
- Zadania (KROKI): docs/tasks.md
- Wizja i zakres: docs/product/vision-and-scope.md
- Wymagania: docs/requirements/
- Decyzje architektoniczne: docs/adr/
- Organizacja pracy: docs/team/
- Sprinty: docs/sprints/
- DPIA: docs/dpia.md

## Jak uruchomić
Szkielet aplikacji jest w trakcie tworzenia. Docelowo:
```bash
cp .env.example .env
docker compose up
```

## Praca z repozytorium
Zasady: docs/team/git-workflow.md. Zmiany tylko przez pull request do `develop`.