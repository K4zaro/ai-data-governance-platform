# ADR-0001: Modularny monolit
- **Status:** Propozycja
- **Kontekst:** Zespół 5 osób, dwa semestry; potrzebna jedna transakcyjna baza dla audit logu i workflow.
- **Decyzja:** Jedna aplikacja Django podzielona na moduły (apps): catalog, quality, compliance, workflow, audit, accounts.
- **Rozważane alternatywy:** Mikroserwisy (Kafka, gRPC): duży narzut CI/CD, transakcji rozproszonych i duplikacji modeli.
- **Konsekwencje:** + prostota wdrożenia i testów, jedna baza ACID; − moduły muszą pilnować granic (brak zależności cyklicznych).
- **Autor i data:** 