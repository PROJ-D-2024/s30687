# Opis zbiorów danych

## 1. Dane tabularne

**Nazwa:** Public Health Scotland – GP Practice List Sizes  

**Źródło:** 
https://www.opendata.nhs.scot/

**Opis:**  
Zbiór danych zawiera kwartalne statystyki dotyczące liczby pacjentów zapisanych do praktyk lekarzy pierwszego kontaktu (General Practitioner – GP) w Szkocji.

**Zakres czasowy:**  
2014-01-01 – 2021-07-01

**Rozmiar zbioru:**  
83 391 wierszy × 23 kolumny

**Najważniejsze zmienne:**

- `Date` – data obserwacji (kwartał)
- `PracticeCode` – identyfikator praktyki GP
- `HB` – Health Board
- `HSCP` – Health and Social Care Partnership
- `Sex` – kategoria płci (All / Male / Female)
- `AllAges` – całkowita liczba pacjentów
- `Ages0to4 … Ages85plus` – liczebność pacjentów w grupach wiekowych

**Cel wykorzystania w projekcie:**  
Zbiór danych jest wykorzystywany do analizy struktury demograficznej populacji pacjentów w praktykach GP oraz do budowy cech opisujących zmiany liczby pacjentów w czasie.

---

## 2. Dane tekstowe

**Nazwa:** Raporty Public Health Scotland oraz GP Workforce Survey

**Źródła:**

https://www.knowledge.scot.nhs.uk/media/lzwjbdzt/ph-digest-jan-25.pdf

https://publichealthscotland.scot/publications/general-practice-workforce-survey/general-practice-workforce-survey-2022/
**Opis:**  
Zbiór danych tekstowych składa się z fragmentów raportów oraz biuletynów dotyczących funkcjonowania systemu ochrony zdrowia, statystyk publicznych oraz zasobów kadrowych w opiece zdrowotnej.

Teksty zostały podzielone na sekcje stanowiące jednostki analizy w procesie eksploracyjnej analizy danych.

**Preprocessing:**

- ekstrakcja tekstu z dokumentów
- normalizacja tekstu (lowercase)
- tokenizacja
- usunięcie stop-słów

**Rozmiar korpusu:**

- liczba dokumentów / sekcji: 14
- liczba unikalnych słów: 1127
- średnia długość dokumentu: około 290 tokenów

**Cel wykorzystania w projekcie:**  
Korpus tekstowy służy do identyfikacji dominujących tematów oraz słów kluczowych związanych z funkcjonowaniem systemu opieki zdrowotnej. W analizie zastosowano metody takie jak analiza częstości słów, TF-IDF oraz modelowanie tematów (LDA).

---

## Wykorzystanie danych

Dane tabularne dostarczają informacji demograficznych i statystycznych dotyczących praktyk GP, natomiast dane tekstowe stanowią kontekst opisowy związany z funkcjonowaniem systemu ochrony zdrowia. Połączenie obu typów danych umożliwia szerszą analizę oraz przygotowanie cech do dalszego modelowania w ramach pracy dyplomowej.