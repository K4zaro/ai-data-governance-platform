# spec.md: Platforma oceny i zarządzania jakością danych (Data Governance & AI Act)

| | |
|---|---|
| **Status** | DRAFT v0.1 (do przeglądu zespołu w PR) |
| **Zakres wydania** | MVP (PZ2) + rozszerzenia oznaczone *Should/Could* |
| **Powiązane dokumenty** | `plan.md` (JAK), `tasks.md` (KROKI), `docs/adr/` (decyzje), `docs/dpia.md` |
| **Zasada zmian** | Zmiana wymagań = najpierw PR do tego pliku, potem plan i zadania |

> **Jak czytać ten dokument.** `spec.md` opisuje **CO i DLACZEGO**. Nie opisuje stosu technologicznego ani struktury kodu (to `plan.md`). Każde wymaganie ma stabilne ID, priorytet (MoSCoW) i testowalne kryteria akceptacji, z których wyprowadzamy testy.

---

## 1. Cel i kontekst

### 1.1 Problem
Organizacje budujące modele AI i analizy zaawansowane nie mają systematycznej odpowiedzi na pytania: *jakie dane mamy, jakiej są jakości, czy wolno ich użyć do tego konkretnego celu i kto za to odpowiada*. Skutkiem są błędne wyniki modeli, ryzyko niezgodności z AI Act (m.in. art. 10, wymogi dla danych w systemach wysokiego ryzyka) i RODO (m.in. art. 5, 6, 9, 35) oraz rozproszona odpowiedzialność.

### 1.2 Cel produktu
Platforma webowa, która:
1. **inwentaryzuje** zbiory danych i ich metadane (w tym pochodzenie),
2. **mierzy jakość** zbiorów w pięciu wymiarach,
3. **wspiera ocenę zgodności** (AI Act, RODO) przez kwestionariusze i listy kontrolne,
4. **kontroluje wykorzystanie** zbiorów w projektach AI przez wieloetapowy, audytowalny workflow zatwierdzeń.

### 1.3 Mierzalne cele (kryteria sukcesu projektu)
| ID | Cel | Miara |
|---|---|---|
| G-1 | Pełny przepływ end-to-end działa na demo | Scenariusz S-1 (sekcja 9) przechodzi w < 5 min bez ręcznych poprawek w bazie |
| G-2 | Jakość liczona automatycznie | Wynik DQS dla zbioru 100 tys. wierszy w < 15 s (NFR-3) |
| G-3 | Brak ominięcia wymaganego etapu zatwierdzenia | 0 ścieżek w testach, w których wniosek z PII osiąga APPROVED bez etapu DPO |
| G-4 | Odtwarzalność | `docker compose up` uruchamia system z danymi demo |

### 1.4 Zakres i poza zakresem
**W zakresie (MVP):** katalog, upload CSV, profilowanie, wykrywanie PII, 5 wymiarów jakości, dashboard, kwestionariusz ryzyka AI Act, lista kontrolna RODO, workflow z audit trail, RBAC.

**Poza zakresem tego wydania (świadomie):**
- porady prawne i automatyczne orzekanie o zgodności (platforma jest **narzędziem wspierającym**, decyzję podejmuje człowiek),
- automatyczne wykrywanie lineage z zewnętrznych systemów (lineage jest wprowadzany ręcznie),
- trenowanie, hosting i monitoring modeli AI,
- multi-tenant, billing, integracje SSO poza ustaloną w ADR,
- konektory do systemów produkcyjnych inne niż wskazane jako *Could*.

### 1.5 Założenia i ograniczenia
- A-1. Dane testowe i demo są **wyłącznie syntetyczne**.
- A-2. Platforma przechowuje metadane, statystyki i zamaskowane próbki (maks. 100 wierszy). Surowe pliki trzymane są w magazynie za interfejsem `Storage` (NFR-1).
- A-3. Klasyfikacja ryzyka AI Act opiera się na uproszczonym drzewie decyzyjnym wersjonowanym w repo i **wymaga weryfikacji prawnej** przed użyciem poza projektem dydaktycznym.
- A-4. Czas projektu: 2 semestry; PZ1 = projektowanie, PZ2 = realizacja (do potwierdzenia z prowadzącym, patrz sekcja 10).

---

## 2. Słownik pojęć

| Termin | Znaczenie |
|---|---|
| **Zbiór danych (Dataset)** | Zarejestrowany w katalogu plik lub tabela z metadanymi |
| **Wersja zbioru** | Niezmienny zrzut zbioru (plik + schemat + profil) w danym momencie |
| **Przebieg jakości (Quality Run)** | Jednorazowe obliczenie wymiarów jakości dla wersji zbioru |
| **DQS** | Total Data Quality Score, ważona średnia pięciu wymiarów (0–100%) |
| **PII** | Dane osobowe; **SENSITIVE** = szczególne kategorie (art. 9 RODO) |
| **Wniosek (Access Request)** | Prośba o użycie wersji zbioru w projekcie AI/analitycznym |
| **Projekt AI** | Opisany cel, model i horyzont czasowy, dla którego składany jest wniosek |
| **Ocena ryzyka AI** | Wynik kwestionariusza: UNACCEPTABLE / HIGH / LIMITED / MINIMAL |
| **Audit trail** | Niezmienny (append-only) dziennik zdarzeń |

---

## 3. Aktorzy i uprawnienia

| Rola | Opis | Kluczowe uprawnienia |
|---|---|---|
| **AI_ENGINEER** (wnioskodawca) | Analityk/Data Scientist | Przegląda katalog i jakość, wypełnia kwestionariusz, składa wnioski |
| **DATA_OWNER** | Biznesowo odpowiada za zbiór | Rejestruje zbiory, zatwierdza etap 1 dla swoich zbiorów |
| **DATA_STEWARD** | Opiekun metadanych i jakości | Edytuje metadane, reguły jakości, lineage; zatwierdza etap 2 |
| **COMPLIANCE_OFFICER** | Zgodność prawna | Weryfikuje ocenę AI Act; zatwierdza etap 3 |
| **DPO** (IODO) | Ochrona danych osobowych | Weryfikuje RODO; zatwierdza etap 4 (tylko gdy PII) |
| **ADMIN** | Administracja systemem | Konta, role, progi globalne, podgląd audit trail |

**Zasady przekrojowe:**
- RBAC-1. Użytkownik może mieć wiele ról; uprawnienia sumują się.
- RBAC-2. **Zakaz samo-zatwierdzania:** użytkownik nie może zatwierdzić etapu wniosku, który sam złożył.
- RBAC-3. Owner i Steward są przypisywani **per zbiór** (relacja N:M).

---

## 4. Epiki

| Epik | Nazwa | Priorytet |
|---|---|---|
| E0 | Uwierzytelnianie, RBAC, administracja | Must |
| E1 | Katalog i inwentaryzacja danych | Must |
| E2 | Ocena jakości danych | Must |
| E3 | Ocena zgodności (AI Act, RODO) | Must (bias: Could) |
| E4 | Workflow zatwierdzania | Must |
| E5 | Audyt i raportowanie | Must (PDF: Should) |

---

## 5. Wymagania funkcjonalne: historyjki użytkownika

Notacja kryteriów: **GDY** (kontekst) **GDY** (zdarzenie) **SYSTEM POWINIEN** (rezultat). Każde kryterium musi mieć odpowiadający test w `tests/`.

### E0. Uwierzytelnianie i administracja

#### US-001 Logowanie `[Must]`
Jako użytkownik chcę się zalogować, aby korzystać z funkcji odpowiadających mojej roli.
- GDY podam poprawne dane GDY wyślę formularz SYSTEM POWINIEN wystawić token sesji i przekierować na stronę główną.
- GDY podam błędne dane SYSTEM POWINIEN odmówić logowania, nie ujawniając, czy login istnieje.
- GDY token wygaśnie SYSTEM POWINIEN zażądać ponownego logowania.

#### US-002 Kontrola dostępu wg roli `[Must]`
Jako administrator chcę przypisywać role, aby ograniczyć dostęp do funkcji.
- GDY użytkownik bez wymaganej roli wywoła chronioną operację SYSTEM POWINIEN zwrócić 403 i zapisać próbę w audit trail.
- GDY administrator zmieni rolę SYSTEM POWINIEN zapisać stan przed i po w audit trail.

#### US-003 Przełącznik roli w trybie demo `[Should]`
Jako prezentujący chcę przełączać widok między rolami bez wylogowania, aby przeklikać cały proces na demo.
- GDY tryb demo jest włączony w konfiguracji GDY wybiorę rolę SYSTEM POWINIEN zmienić kontekst uprawnień na wybraną rolę.
- GDY tryb demo jest wyłączony SYSTEM POWINIEN nie pokazywać przełącznika ani nie akceptować nagłówka zmiany roli (**tryb nie może istnieć w konfiguracji produkcyjnej**).

### E1. Katalog i inwentaryzacja

#### US-101 Rejestracja zbioru `[Must]`
Jako Data Owner chcę zarejestrować zbiór z opisem, tagami i plikiem, aby był widoczny w katalogu.
- GDY prześlę plik CSV (do limitu z NFR) z nazwą i opisem SYSTEM POWINIEN utworzyć zbiór z unikalnym UUID i wersją 1.
- GDY plik jest pusty, uszkodzony lub przekracza limit SYSTEM POWINIEN odrzucić go z komunikatem wskazującym przyczynę.
- GDY prześlę nowy plik do istniejącego zbioru SYSTEM POWINIEN utworzyć nową wersję bez nadpisywania poprzednich.
- *Could:* formaty Parquet/JSON, połączenie do tabeli PostgreSQL.

#### US-102 Wyszukiwanie w katalogu `[Must]`
Jako AI Engineer chcę wyszukiwać zbiory po nazwie, opisie, tagach i klasyfikacji.
- GDY wpiszę frazę SYSTEM POWINIEN zwrócić zbiory pasujące do nazwy, opisu lub tagów.
- GDY zastosuję filtr klasyfikacji (PII, SENSITIVE, INTERNAL, PUBLIC) SYSTEM POWINIEN pokazać wyłącznie zbiory zawierające kolumny o tej klasyfikacji.

#### US-103 Automatyczne profilowanie i klasyfikacja kolumn `[Must]`
Jako Data Steward chcę, aby system wykrywał dane osobowe i wrażliwe, aby nie robić tego ręcznie.
- GDY wersja zbioru zostanie zarejestrowana SYSTEM POWINIEN uruchomić profilowanie w tle i pokazać status (PENDING / RUNNING / DONE / FAILED).
- GDY kolumna zawiera wartości o formacie PESEL z poprawną sumą kontrolną, e-mail, telefon, NIP lub IBAN albo nazwa kolumny pasuje do słownika SYSTEM POWINIEN oznaczyć ją jako PII wraz z pewnością detekcji.
- GDY kolumna pasuje do słownika kategorii szczególnych (np. zdrowie, wyznanie, pochodzenie) SYSTEM POWINIEN oznaczyć ją jako SENSITIVE.
- GDY wykryto co najmniej jedną kolumnę PII lub SENSITIVE SYSTEM POWINIEN ustawić `contains_pii = true` dla wersji zbioru.
- GDY Data Steward zmieni klasyfikację kolumny SYSTEM POWINIEN zapisać zmianę z uzasadnieniem w audit trail i ten ręczny wybór ma pierwszeństwo przed automatycznym.
- Profilowanie **nie może** zapisywać w bazie pełnych wartości PII; próbka ma maks. 100 wierszy z maskowaniem.

#### US-104 Przypisanie Ownera i Stewarda `[Must]`
Jako administrator lub Owner chcę przypisać odpowiedzialnych do zbioru.
- GDY zbiór nie ma co najmniej jednego Ownera i jednego Stewarda SYSTEM POWINIEN uniemożliwić nadanie statusu ACTIVE.
- GDY zbiór nie jest ACTIVE SYSTEM POWINIEN uniemożliwić złożenie wniosku o jego użycie.

#### US-105 Lineage ręczny `[Should]`
Jako Data Steward chcę opisać pochodzenie zbioru jako graf: źródło → transformacja → zbiór → projekt AI.
- GDY dodam krawędź SYSTEM POWINIEN zapisać ją ze źródłem, celem i opisem transformacji.
- GDY dodana krawędź utworzyłaby cykl SYSTEM POWINIEN ją odrzucić.
- GDY otworzę kartę zbioru SYSTEM POWINIEN wyświetlić graf pochodzenia.

### E2. Ocena jakości

#### US-201 Obliczenie wymiarów jakości `[Must]`
Jako Data Steward chcę automatycznej oceny jakości, aby obiektywnie opisać zbiór.
- GDY wersja zbioru zostanie sprofilowana SYSTEM POWINIEN obliczyć pięć wymiarów (0–100%) i DQS.
- GDY zbiór ma do 100 tys. wierszy SYSTEM POWINIEN zakończyć obliczenia w < 15 s i nie blokować API.
- GDY obliczenie się nie powiedzie SYSTEM POWINIEN zapisać status FAILED z przyczyną, a nie częściowy wynik.
- Definicje wymiarów: sekcja 6.

#### US-202 Reguły jakości `[Must]`
Jako Data Steward chcę definiować reguły dla poprawności i spójności bez zmian w kodzie.
- GDY dodam regułę typu *wzorzec*, *zakres*, *słownik wartości* lub *relacja między kolumnami* SYSTEM POWINIEN zastosować ją przy kolejnym przebiegu.
- GDY reguła jest niepoprawna składniowo SYSTEM POWINIEN odrzucić ją przy zapisie z komunikatem.
- GDY zbiór nie ma reguł dla wymiaru SYSTEM POWINIEN oznaczyć wymiar jako *nieoceniony* (nie jako 100%).

#### US-203 Dashboard jakości `[Must]`
Jako AI Engineer chcę zobaczyć jakość zbioru, aby ocenić jego przydatność.
- GDY otworzę dashboard zbioru SYSTEM POWINIEN pokazać pięć wymiarów, DQS, datę przebiegu i wersję zbioru.
- GDY istnieje więcej niż jeden przebieg SYSTEM POWINIEN pokazać trend w czasie.
- GDY wymiar jest poniżej progu SYSTEM POWINIEN wyróżnić go wizualnie i wskazać kolumny o największym udziale w defektach.

#### US-204 Progi i alerty `[Should]`
Jako Data Steward chcę alertów o spadku jakości.
- GDY wymiar lub DQS spadnie poniżej progu (domyślnie: kompletność 95%, DQS 80%; konfigurowalne) SYSTEM POWINIEN utworzyć powiadomienie w aplikacji dla Stewarda zbioru.
- GDY alert jest aktywny SYSTEM POWINIEN oznaczyć zbiór jako *wymagający uwagi* i uwzględnić to w workflow (US-403).
- *Could:* powiadomienie e-mail.

#### US-205 Rekomendacje naprawcze `[Should]`
Jako Data Steward chcę wskazówek, co poprawić.
- GDY wykryto defekt w wymiarze SYSTEM POWINIEN zaproponować rekomendację z szablonu wraz z konkretnymi liczbami (kolumna, % braków, liczba duplikatów).
- Rekomendacje są **sugestiami**; system nie modyfikuje danych źródłowych.

### E3. Ocena zgodności

#### US-301 Kwestionariusz ryzyka AI Act `[Must]`
Jako AI Engineer chcę sklasyfikować mój system AI, aby wiedzieć, jakie obowiązki go dotyczą.
- GDY odpowiem na pytania o domenę zastosowania i funkcję systemu SYSTEM POWINIEN wyznaczyć klasę: UNACCEPTABLE, HIGH, LIMITED lub MINIMAL wraz z uzasadnieniem (które odpowiedzi doprowadziły do wyniku).
- GDY wynik to UNACCEPTABLE SYSTEM POWINIEN uniemożliwić złożenie wniosku.
- GDY wynik to HIGH SYSTEM POWINIEN włączyć dodatkową listę kontrolną z US-302.
- GDY zmieni się wersja drzewa decyzyjnego SYSTEM POWINIEN zachować wersję użytą w historycznych ocenach.
- System **zawsze** pokazuje zastrzeżenie, że wynik nie stanowi porady prawnej.

#### US-302 Lista kontrolna wymogów dla danych w systemach wysokiego ryzyka `[Must]`
Jako Compliance Officer chcę sprawdzić, czy zbiór spełnia wymogi dotyczące danych treningowych (art. 10).
- GDY ocena ryzyka to HIGH SYSTEM POWINIEN wyświetlić listę kontrolną (pochodzenie danych, dokumentacja przygotowania, reprezentatywność, badanie możliwych uprzedzeń, luki i braki).
- GDY element listy jest niezaznaczony SYSTEM POWINIEN pokazać go jako brak i uwzględnić w raporcie.
- Pozycje listy są konfigurowalne (plik w repo, wersjonowany).

#### US-303 Lista kontrolna RODO `[Must]`
Jako DPO chcę zweryfikować podstawę prawną i minimalizację danych.
- GDY zbiór zawiera PII SYSTEM POWINIEN wymagać wskazania podstawy prawnej (art. 6) oraz, dla SENSITIVE, warunku z art. 9.
- GDY kolumna PII nie jest oznaczona jako niezbędna do celu projektu SYSTEM POWINIEN wskazać ją jako kandydata do maskowania lub usunięcia (minimalizacja).
- GDY brakuje określonego celu lub okresu retencji SYSTEM POWINIEN oznaczyć listę jako niekompletną.
- *Should:* dla zbiorów z PII wysokiego ryzyka system podpowiada konieczność DPIA (art. 35) jako element listy.

#### US-304 Reprezentatywność i bias `[Could]`
Jako Compliance Officer chcę zobaczyć rozkład grup chronionych.
- GDY użytkownik wskaże kolumnę atrybutu chronionego (np. płeć, wiek w przedziałach) i kolumnę wyniku SYSTEM POWINIEN policzyć udziały grup oraz Disparate Impact Ratio.
- GDY DIR jest poza przedziałem 0,8–1,25 (konfigurowalny) SYSTEM POWINIEN pokazać ostrzeżenie.
- Wynik jest sygnałem do analizy, nie dowodem dyskryminacji.

### E4. Workflow zatwierdzania

#### US-401 Złożenie wniosku `[Must]`
Jako AI Engineer chcę złożyć wniosek o użycie zbioru w projekcie AI.
- GDY wskażę aktywną wersję zbioru, cel, model, horyzont czasowy i ukończony kwestionariusz AI Act SYSTEM POWINIEN utworzyć wniosek w stanie SUBMITTED powiązany z tą wersją.
- GDY brakuje któregokolwiek z powyższych SYSTEM POWINIEN odrzucić zgłoszenie z listą braków.
- GDY ocena ryzyka to UNACCEPTABLE SYSTEM POWINIEN odrzucić zgłoszenie.

#### US-402 Maszyna stanów weryfikacji `[Must]`
Jako system chcę wymusić kolejność zatwierdzeń.
- Kolejność etapów: **Owner → Steward → Compliance → DPO (tylko gdy `contains_pii = true`) → APPROVED**.
- GDY etap Ownera zostanie zatwierdzony SYSTEM POWINIEN przekazać wniosek do Stewarda (analogicznie dalej).
- GDY zbiór nie zawiera PII SYSTEM POWINIEN pominąć etap DPO.
- GDY zatwierdzający odrzuci wniosek SYSTEM POWINIEN ustawić stan REJECTED (stan końcowy).
- GDY zatwierdzający cofnie wniosek do poprawy SYSTEM POWINIEN ustawić RETURNED i umożliwić wnioskodawcy edycję oraz ponowne złożenie, po czym proces **zaczyna się od etapu 1**.
- GDY ktoś spróbuje wykonać przejście niedozwolone przez maszynę stanów SYSTEM POWINIEN je odrzucić (409) i nie zmienić stanu.
- GDY użytkownik nie jest przypisany do danego etapu lub zbioru SYSTEM POWINIEN odmówić (403).
- Test własności (G-3): dla każdej ścieżki wniosek z PII nie może osiągnąć APPROVED bez decyzji DPO.

#### US-403 Bramki jakości w workflow `[Should]`
Jako Data Steward chcę, aby słaba jakość zatrzymywała wniosek.
- GDY zbiór ma aktywny alert jakości SYSTEM POWINIEN wymagać od Stewarda jawnego uzasadnienia przy zatwierdzeniu (świadome zatwierdzenie z odchyleniem).
- GDY ostatni przebieg jakości jest starszy niż SLA odświeżania SYSTEM POWINIEN ostrzec zatwierdzającego.

#### US-404 Kolejka zadań zatwierdzającego `[Must]`
Jako zatwierdzający chcę widzieć wnioski oczekujące na moją decyzję.
- GDY otworzę kolejkę SYSTEM POWINIEN pokazać wyłącznie wnioski, w których aktualny etap odpowiada mojej roli i zbiorom, za które odpowiadam.
- GDY wniosek zmieni stan SYSTEM POWINIEN powiadomić (w aplikacji) wnioskodawcę oraz następnego zatwierdzającego.

#### US-405 Decyzja z uzasadnieniem `[Must]`
Jako zatwierdzający chcę podjąć decyzję z uzasadnieniem.
- GDY zatwierdzę, odrzucę lub cofnę wniosek bez uzasadnienia SYSTEM POWINIEN odmówić zapisu.
- GDY zapiszę decyzję SYSTEM POWINIEN zapisać etap, decyzję, uzasadnienie, autora i czas UTC w historii.
- GDY wniosek jest w stanie końcowym SYSTEM POWINIEN uniemożliwić dalsze decyzje.

### E5. Audyt i raportowanie

#### US-501 Niezmienny dziennik zdarzeń `[Must]`
Jako administrator chcę mieć niezmienny dziennik, aby spełnić wymagania audytowe.
- GDY zmieni się klasyfikacja danych, reguły jakości, rola użytkownika lub stan wniosku SYSTEM POWINIEN dopisać wpis: kto, co, kiedy (UTC), stan przed, stan po (+ adres IP jeśli dostępny).
- GDY ktokolwiek (także administrator) spróbuje zmienić lub usunąć wpis SYSTEM POWINIEN to uniemożliwić na poziomie aplikacji **i** bazy danych (brak uprawnień UPDATE/DELETE dla konta aplikacji).

#### US-502 Certyfikat zgodności danych (PDF) `[Should]`
Jako AI Engineer chcę pobrać potwierdzenie zatwierdzenia na potrzeby audytu.
- GDY wniosek ma stan APPROVED SYSTEM POWINIEN wygenerować PDF z identyfikatorem wniosku, wersją zbioru, wynikami jakości, oceną ryzyka i pełną ścieżką decyzji.
- GDY wniosek nie jest APPROVED SYSTEM POWINIEN nie udostępniać certyfikatu.

#### US-503 Przegląd historii wniosku `[Must]`
Jako uczestnik procesu chcę zobaczyć pełną historię decyzji wniosku.
- GDY otworzę wniosek SYSTEM POWINIEN pokazać chronologiczną listę decyzji z uzasadnieniami.

---

## 6. Definicje wymiarów jakości (reguły obliczeń)

> Wzory są założeniem zespołu do zatwierdzenia w ADR. Pięć wymiarów jest powszechnie stosowanym zestawem w literaturze data quality (m.in. DAMA); źródło cytowane na obronie należy zweryfikować.

| Wymiar | Definicja | Uwagi |
|---|---|---|
| **Kompletność** | `(1 − N_puste / N_komórek) × 100`; puste = NULL, NaN, pusty ciąg, ciąg białych znaków | liczona globalnie i per kolumna |
| **Unikalność** | `N_unikalnych_wierszy / N_wierszy × 100`; per kolumna dla kluczy | klucz biznesowy wskazuje Steward |
| **Poprawność** | `N_rekordów_zgodnych_z_regułami / N_ocenianych × 100` | tylko kolumny z regułami (wzorzec, zakres, słownik) |
| **Spójność** | `N_rekordów_spełniających_relacje / N_ocenianych × 100` | reguły relacji między kolumnami |
| **Aktualność** | `100` gdy `wiek ≤ SLA`; w przeciwnym razie `max(0, 100 × (1 − (wiek − SLA) / SLA))` | `wiek` = teraz − czas ostatniej aktualizacji; SLA ustala Steward |
| **DQS** | średnia ważona ocenionych wymiarów; domyślnie wagi równe, konfigurowalne | wymiary *nieocenione* nie wchodzą do średniej i są pokazane jawnie |

---

## 7. Wymagania niefunkcjonalne

| ID | Kategoria | Wymaganie | Sposób weryfikacji |
|---|---|---|---|
| NFR-01 | Prywatność (Privacy by Design) | W bazie wyłącznie metadane, statystyki, schematy i maskowane próbki (maks. 100 wierszy). Surowe pliki w magazynie za interfejsem `Storage`; szyfrowanie w spoczynku w środowisku docelowym | Test: brak wartości PII w tabelach i logach |
| NFR-02 | Audytowalność | Append-only audit log (US-501) | Test uprawnień DB |
| NFR-03 | Wydajność | Profilowanie i jakość dla ≤ 100 tys. wierszy w < 15 s, asynchronicznie | Test wydajnościowy na danych syntetycznych |
| NFR-04 | Przenośność | Uruchomienie jednym poleceniem `docker compose up` wraz z danymi demo | Weryfikacja na czystej maszynie |
| NFR-05 | Bezpieczeństwo | Hasła haszowane (bcrypt/argon2), tokeny wygasające, walidacja wejścia, limity rozmiaru plików, brak sekretów w repo, wykonywanie reguł użytkownika **bez** `eval` | Przegląd kodu, skan zależności |
| NFR-06 | Jakość kodu | CI: lint + testy na każdy PR; pokrycie testami reguł jakości i maszyny stanów ≥ 80% | Pipeline CI |
| NFR-07 | Dostępność UI | Podstawowa zgodność z WCAG 2.1 AA (kontrast, nawigacja klawiaturą, etykiety) | Lighthouse/axe |
| NFR-08 | Utrzymywalność | Podział na moduły domenowe (catalog, quality, compliance, workflow); brak zależności cyklicznych między modułami | Przegląd architektury |
| NFR-09 | Dokumentacja API | Specyfikacja OpenAPI generowana i aktualna | Test zgodności w CI |
| NFR-10 | Lokalizacja | Interfejs w języku polskim; ciągi tekstowe poza kodem (gotowość do i18n) | Przegląd |

---

## 8. Dane i kontrakty (poziom specyfikacji)

> Szczegóły (typy kolumn, indeksy, endpointy) trafiają do `plan.md` i OpenAPI. Tu tylko to, co wynika z wymagań.

**Encje:** User, Role (N:M), Dataset, DatasetVersion, DatasetColumn, DatasetOwnership (Owner/Steward, N:M), LineageEdge, QualityRule, QualityRun (wyniki per wymiar i per kolumna), AiProject, RiskQuestionnaireVersion, RiskAssessment, ComplianceChecklistItem/Answer, AccessRequest, ApprovalDecision, Notification, AuditLogEntry, Job (zadania w tle).

**Niezmienniki:**
- Wniosek wskazuje **konkretną wersję** zbioru i konkretną ocenę ryzyka.
- ApprovalDecision i AuditLogEntry są niezmienne po zapisie.
- `contains_pii` jest atrybutem wersji zbioru, a nie zbioru.

**Kontrakt API:** REST + JSON, specyfikacja OpenAPI, błędy w ujednoliconym formacie (kod, komunikat, szczegóły pól), operacje długie zwracają `202 Accepted` + identyfikator zadania.

---

## 9. Scenariusze akceptacyjne end-to-end

**S-1 (główny, demo).** Owner rejestruje zbiór (z PII) → system profiluje i flaguje kolumny → Steward zatwierdza klasyfikację i dodaje reguły → system liczy jakość → AI Engineer wypełnia kwestionariusz (wynik HIGH) → składa wniosek → Owner, Steward, Compliance i DPO zatwierdzają kolejno → wniosek APPROVED → audit trail zawiera wszystkie kroki.

**S-2 (ścieżka bez PII).** Zbiór bez PII: wniosek przechodzi trzy etapy, etap DPO jest pominięty.

**S-3 (odrzucenie).** Compliance odrzuca z uzasadnieniem: wniosek REJECTED, brak możliwości dalszych decyzji.

**S-4 (cofnięcie).** Steward cofa wniosek do poprawy → wnioskodawca poprawia → proces startuje od etapu 1.

**S-5 (jakość poniżej progu).** Nowa wersja zbioru ma kompletność < 95% → alert → zatwierdzenie przez Stewarda wymaga uzasadnienia.

**S-6 (próba obejścia).** Wnioskodawca próbuje zatwierdzić własny wniosek lub pominąć etap: 403/409, zdarzenie w audit trail.

---

## 10. Ryzyka i otwarte pytania

| ID | Ryzyko / pytanie | Plan |
|---|---|---|
| R-1 | Zakres zbyt szeroki na 2 semestry | MoSCoW; *Should/Could* są pierwsze do cięcia |
| R-2 | Błędna interpretacja AI Act | Drzewo decyzyjne weryfikowane z prawnikiem/prowadzącym; zastrzeżenie w UI |
| R-3 | Fałszywe trafienia/pominięcia detekcji PII | Pewność detekcji + ręczna korekta (US-103) |
| R-4 | Zbyt złożona infrastruktura | Najprostsza architektura spełniająca NFR; decyzje w ADR |
| R-5 | Użycie LLM bez weryfikacji | Każdy artefakt ma autora, który za niego odpowiada; przegląd w PR |
| Q-1 | Czy PZ1 ma zawierać kod (szkielet)? | Do potwierdzenia z prowadzącym |
| Q-2 | Dane osobowe w samym systemie: czy wymagane DPIA dla naszej platformy? | Ustalić zakres; przy danych syntetycznych wersja skrócona |
| Q-3 | Czy lineage automatyczny jest oczekiwany? | Zakładamy: nie (poza zakresem) |
| Q-4 | Czy jest wymagane LDAP/SSO? | Do uzgodnienia; domyślnie lokalne konta |
| Q-5 | Czy bias (US-304) wchodzi do MVP? | Decyzja zespołu na planningu sprintu 2 |

---

## 11. Macierz śledzenia (wymaganie → epik → priorytet)

| Cel produktu | Historyjki |
|---|---|
| Inwentaryzacja | US-101…105 |
| Jakość | US-201…205 |
| Zgodność | US-301…304 |
| Kontrola użycia | US-401…405 |
| Audyt | US-501…503 |
| Platforma | US-001…003 |

**Definition of Done dla historyjki:** kod + testy wyprowadzone z kryteriów akceptacji + zaktualizowany `spec.md` (jeśli zmieniono wymaganie) + przegląd w PR + działa w `docker compose up`.

---

## 12. Historia zmian

| Wersja | Data | Autor | Zmiana |
|---|---|---|---|
| 0.1 | 2026-11-04 | *(uzupełnić)* | Pierwsza wersja robocza |
