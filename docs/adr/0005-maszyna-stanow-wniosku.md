# ADR-0005: Jawna maszyna stanów wniosku
- **Status:** Propozycja
- **Kontekst:** Etap IOD jest warunkowy (`contains_pii`), są cofnięcia i odrzucenia, a wniosek z PII nie może ominąć IOD (cel G-3).
- **Decyzja:** Stany: OWNER_REVIEW, STEWARD_REVIEW, COMPLIANCE_REVIEW, DPO_REVIEW, RETURNED, APPROVED, REJECTED. Dozwolone przejścia w jednej tabeli/funkcji; każde przejście zapisuje decyzję z uzasadnieniem i wpis w audit logu.
- **Rozważane alternatywy:** Flagi boolean (`is_owner_approved` itd.): trudne do utrzymania i łatwo ominąć etap.
- **Konsekwencje:** + testowalny model, test własności dla ścieżek z PII; − trzeba utrzymywać tabelę przejść.
- **Autor i data:**