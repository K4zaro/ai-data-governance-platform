# Platforma Data Governance & AI Act Compliance

Platforma webowa do oceny jakości i zarządzania zgodnością zbiorów danych używanych w systemach AI.

## Zespół

| Osoba            | Rola / obszar |
| ---------------- | ------------- |
| Kamil Osakowicz  |               |
| Radek Kulesza    |               |
| Michał Spaliński |               |
| Filip Kamiński   |               |
| Konrad Zajczyk   |               |

## Linki

- Jira: [link]
- Confluence: [link]
- Teams: [kanał]

## Stos technologiczny

Python 3.12, Django 5.2 LTS, szablony + HTMX, Bootstrap 5, Chart.js, Celery + Redis, pandas, PostgreSQL 16, Docker Compose.

## Architektura

Aplikacja oparta jest na Django i podzielona na sześć modułów:

- `accounts` – użytkownicy i uprawnienia
- `catalog` – katalog zbiorów danych
- `quality` – ocena jakości danych
- `compliance` – zgodność z AI Act i RODO
- `workflow` – wnioski i proces zatwierdzania
- `audit` – rejestrowanie operacji

Środowisko Docker Compose obejmuje cztery usługi:

- `web` – aplikacja Django
- `worker` – zadania asynchroniczne Celery
- `postgres` – baza danych PostgreSQL
- `redis` – broker wiadomości Celery

## Dokumentacja

- Specyfikacja (CO i DLACZEGO): [docs/spec.md](docs/spec.md)
- Plan (JAK): [docs/plan.md](docs/plan.md)
- Zadania (KROKI): [docs/tasks.md](docs/tasks.md)
- Wizja i zakres: [docs/product/vision-and-scope.md](docs/product/vision-and-scope.md)
- Wymagania: [docs/requirements/](docs/requirements/)
- Decyzje architektoniczne: [docs/adr/](docs/adr/)
- Organizacja pracy: [docs/team/](docs/team/)
- Sprinty: [docs/sprints/](docs/sprints/)
- DPIA: [docs/dpia.md](docs/dpia.md)

## Jak uruchomić

### Wymagania

- Git
- Docker Desktop z WSL 2 (Windows) lub Docker Engine z Docker Compose (Linux)

### Konfiguracja

1. Sklonuj repozytorium.
2. Skopiuj `.env.example` do `.env`.
3. W pliku `.env` uzupełnij `POSTGRES_PASSWORD` oraz `DJANGO_SECRET_KEY` silnymi, losowo wygenerowanymi wartościami.

Przykładowe generowanie wartości w PowerShell:

```powershell
$bytes = New-Object byte[] 48
$rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
$rng.GetBytes($bytes)
$rng.Dispose()

[BitConverter]::ToString($bytes).Replace("-", "")
```

Uruchom polecenie dwukrotnie, aby wygenerować osobne wartości dla hasła PostgreSQL i klucza Django.

Plik `.env` jest wykluczony z repozytorium przez `.gitignore` i nie powinien być commitowany.

### Uruchomienie

```bash
docker compose up --build -d
docker compose exec web python manage.py migrate
```

Aplikacja dostępna jest pod adresem:

http://localhost:8000

### Zatrzymanie

```bash
docker compose down
```

Dane PostgreSQL przechowywane są w woluminie Dockera i pozostają zachowane po zatrzymaniu kontenerów.

## Praca z repozytorium

Zasady: [docs/team/git-workflow.md](docs/team/git-workflow.md).

Zmiany wprowadzane są na osobnych gałęziach i łączone z `develop` wyłącznie przez Pull Request.
