# Working Agreement

## Sprint
- Długość sprintu: 2 tygodnie **[DO USTALENIA]**.
- Do sprintu wchodzą **tylko tickety wycenione w story pointach**; każdy ticket ma jedną osobę odpowiedzialną.
- Sufit prędkości: 60 SP. W pierwszym sprincie planujemy 40-50 SP, potem korygujemy według rzeczywistej prędkości.
- Każdy sprint ma: cel, Product Ownera, review, retrospektywę i notatki ze statusów.
- Product Owner zmienia się co sprint (rotacja ustalona z góry).

## Narzędzia
- Jira: zadania i sprinty. Confluence: wiedza i dokumentacja. GitHub: kod. Teams: komunikacja.
- Każda zmiana w kodzie jest powiązana z ticketem w Jirze (klucz w nazwie gałęzi i commicie).

## Komunikacja
- Statusy: 2-3 razy w tygodniu, krótki wpis na kanale zespołu w Teams (co zrobiłem, co robię, co blokuje).
- Pytania blokujące zgłaszamy od razu.

## Definition of Done (zadanie z kodem)
- Kod trafił do `develop` przez pull request z review innej osoby.
- Testy przechodzą w CI.
- Kryteria akceptacji sprawdzone przez inną osobę.
- Migracje działają na czystej bazie.
- Nowe widoki mają sprawdzone uprawnienia ról.
- Dokumentacja i `spec.md` są aktualne, jeśli zmieniła się funkcja.

## Definition of Done (zadanie dokumentacyjne)
- Strona/plik ma autora i status.
- Przeczytana i zaakceptowana przez co najmniej jedną inną osobę.

## Estymacja
- Skala Fibonacciego (1, 2, 3, 5, 8, 13), Planning Poker.
- Ticket referencyjny: **[DO USTALENIA]** (np. „założenie repo i dodanie prowadzącego” = 2 SP).
- Ticket powyżej 8 SP dzielimy.

## Zasady korzystania z narzędzi AI
- AI generuje szkice; **konkretna osoba je czyta, poprawia i odpowiada za nie na review**.
- Każdy ADR i każda historyjka ma autora.
- Treści prawne (AI Act, RODO) weryfikujemy w źródłach, a nie w odpowiedziach modelu.
- Zmiana wymagań: najpierw PR do `docs/spec.md`, potem plan i zadania.