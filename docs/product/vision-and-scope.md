## Product Vision & Scope
 
**Status:** Propozycja · **Wersja:** 0.1 · **Autor:** Konrad Zajczyk
 
### 1. Wizja
Platforma, która pozwala organizacji szybko i wiarygodnie odpowiedzieć na pytania: *jakie dane mamy, jakiej są jakości i czy wolno ich użyć w konkretnym projekcie AI*, oraz zapewnia, że decyzja o użyciu danych jest podjęta przez odpowiednie osoby i udokumentowana.
 
### 2. Problem
- Brak przejrzystości: pracownicy nie wiedzą, które dane można bezpiecznie używać do analiz i modeli AI.
- Ryzyko niezgodności z regulacjami (AI Act, RODO) przy braku systematycznej oceny danych.
- Niska jakość danych (braki, duplikaty, nieaktualność) prowadząca do błędnych wyników.
- Brak dokumentacji pochodzenia i charakterystyki danych.
- Rozproszona odpowiedzialność między właścicielami danych, opiekunami, compliance i inspektorem ochrony danych.
### 3. Użytkownicy
| Rola | Czego potrzebuje |
|---|---|
| AI Engineer / Data Scientist | Znaleźć zbiór, ocenić jego jakość, uzyskać zgodę na użycie |
| Data Owner | Kontrolować, kto używa jego danych |
| Data Steward | Utrzymywać metadane i jakość |
| Compliance Officer | Zweryfikować zgodność z AI Act |
| DPO (IODO) | Zweryfikować zgodność z RODO dla danych osobowych |
| Administrator | Zarządzać kontami i rolami |
 
### 4. Cele produktu
1. Jeden katalog zbiorów danych z metadanymi i klasyfikacją (osobowe / wrażliwe / biznesowe).
2. Mierzalna, automatyczna ocena jakości w pięciu wymiarach.
3. Wsparcie oceny zgodności (kwestionariusz ryzyka AI Act, listy kontrolne AI Act i RODO).
4. Wieloetapowy, audytowalny proces zatwierdzania użycia zbioru w projekcie AI.
### 5. Zakres MVP **[DO USTALENIA]**
| Obszar | W MVP | Poza MVP (rozwój) |
|---|---|---|
| Katalog | Rejestracja zbioru (CSV), wersje, wyszukiwanie, klasyfikacja kolumn, przypisanie Ownera i Stewarda | Parquet/JSON, połączenie z bazą, lineage jako graf |
| Jakość | Kompletność, unikalność, aktualność (automatycznie); poprawność i spójność z reguł; dashboard | Alerty, rekomendacje, e-mail |
| Zgodność | Kwestionariusz ryzyka AI Act (drzewo decyzyjne), listy kontrolne AI Act i RODO | Metryki reprezentatywności i biasu |
| Workflow | Wniosek, maszyna stanów (Owner → Steward → Compliance → DPO jeśli PII), historia decyzji | Certyfikat PDF, bramki jakości |
| Platforma | Logowanie, role (RBAC), audit trail, tryb demo (przełącznik ról) | SSO/LDAP, powiadomienia e-mail |
 
### 6. Poza zakresem
- Udzielanie porad prawnych (narzędzie wspierające decyzję człowieka).
- Automatyczne pozyskiwanie lineage z zewnętrznych systemów.
- Trenowanie, hosting i monitoring modeli AI.
- Obsługa wielu organizacji (multi-tenant).
### 7. Podejście iteracyjne
- Produkt rozwijamy w sprintach; MVP powstaje w kolejnych iteracjach, a nie jednorazowo.
- Rozwój kontynuowany jest w kolejnym semestrze: funkcje z kolumny „poza MVP” trafiają do backlogu i są priorytetyzowane na planningu.
- Po każdym sprincie zakres i priorytety są korygowane na podstawie review i retrospektywy.
- Zmiana wymagań: najpierw aktualizacja dokumentacji wymagań, potem zadania.
### 8. Założenia i ograniczenia
- Dane testowe i demonstracyjne są wyłącznie syntetyczne.
- Platforma przechowuje metadane, statystyki i zamaskowane próbki; nie gromadzi pełnych danych osobowych.
- Klasyfikacja ryzyka AI Act jest uproszczona i wymaga weryfikacji prawnej przed jakimkolwiek użyciem poza projektem dydaktycznym.
- Czas: dwa semestry; semestr 1 to projektowanie i szkielet, semestr 2 to realizacja **[DO POTWIERDZENIA z prowadzącym]**.
### 9. Kryteria sukcesu
- Scenariusz główny działa end-to-end: rejestracja zbioru z danymi osobowymi → profilowanie → ocena jakości → kwestionariusz ryzyka → wniosek → cztery zatwierdzenia → pełna historia decyzji.
- Wniosek ze zbiorem zawierającym dane osobowe nie może zostać zatwierdzony bez decyzji DPO.
- System uruchamia się jednym poleceniem na czystej maszynie.
### 10. Ryzyka
| Ryzyko | Reakcja |
|---|---|
| Zakres za szeroki na 2 semestry | Priorytety MoSCoW; funkcje „poza MVP” są pierwsze do cięcia |
| Błędna interpretacja przepisów | Weryfikacja w źródłach i z prowadzącym; zastrzeżenie w UI |
| Zbyt złożona infrastruktura | Najprostsza architektura spełniająca wymagania; decyzje w ADR |
| Korzystanie z LLM bez weryfikacji | Każdy artefakt ma autora, który za niego odpowiada |
 
---
