# 📊 Pairwise Comparison App

Pairwise Comparison App to aplikacja webowa umożliwiająca przeprowadzanie analiz porównawczych przy użyciu metody AHP (Analytic Hierarchy Process). Aplikacja pozwala na definiowanie kryteriów, dodawanie ekspertów oraz przeprowadzanie analizy wyników.

## 🚀 Funkcje

- Dodawanie alternatyw i kryteriów 🔢

- Wprowadzanie porównań parami przez wielu ekspertów 👥

- Obliczanie rankingów oraz wskaźników spójności 📈

  - Obsługa różnych metod wyliczania rankingu, w tym:

    - TOPSIS
    - Uwzględniający spójność ocen ekspertów
    - Podstawowy z równymi wagami kryteriów

  - Obsługa niekompletnych danych poprzez interpolację brakujących wartości

  - Obliczanie stopnia niespójności macierzy, pozwalające na ocenę jakości wprowadzonych porównań

- Zapis i odczyt modelu z pliku JSON 📂

- Interfejs webowy oparty na Flask 🌐

## 🖥️ Wykorzystane technologie

Aplikacja została zbudowana z wykorzystaniem następujących frameworków i bibliotek:

- Flask 🌐 - framework do tworzenia aplikacji webowych
- Bootstrap 🎨 - framework CSS do responsywnego interfejsu użytkownika
- NumPy 🔢 - operacje na macierzach i obliczenia numeryczne

## 📂 Struktura projektu

```
📂 pairwise_comparsion
├── 📄 AHPModel.py       # Implementacja modelu AHP
├── 📄 flask_app.py      # Aplikacja Flask
├── 📄 model.json        # Przykładowy model w formacie JSON
├── 📄 requirements.txt  # Lista wymaganych bibliotek
├── 📂 static            # Pliki statyczne (CSS, JS, obrazy)
├── 📂 templates         # Szablony HTML
└── 📄 README.md         # Dokumentacja projektu
```

## 🛠 Instalacja

1. **Sklonuj repozytorium**
   ```bash
   git clone https://github.com/Redor144/pairwise_comparsion
   cd pairwise-comparison
   ```
2. **Utwórz i aktywuj wirtualne środowisko**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```
3. **Zainstaluj zależności**
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Uruchamianie aplikacji

```bash
python flask_app.py
```

Aplikacja będzie dostępna pod adresem: http\://localhost:22233

## 👥 Autorzy

📌 Aplikacja została stworzona jako projekt zespołowy z przedmiotu **Metody i algorytmy podejmowania decyzji** prowadzonego na AGH UST.

## 📜 Licencja

Projekt jest dostępny na licencji MIT.

