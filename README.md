# Sklep Internetowy Django

Projekt sklepu internetowego stworzony w ramach zaliczenia kursu. Aplikacja umożliwia przeglądanie produktów, dodawanie ich do koszyka, składanie zamówień oraz przeglądanie historii zakupów przez zalogowanych użytkowników.

## Technologie
* Python 3.13
* Django 4.2
* MySQL (XAMPP)
* HTML5 / CSS3

## Funkcjonalności (Kryteria oceny)
1. **Architektura MVT:** Podział na modele, widoki i szablony.
2. **Modele:** Relacje ForeignKey (Kategorie, Zamówienia) oraz ManyToMany (Tagi).
3. **ORM:** Wykorzystanie agregacji (Sum) do obliczania wartości zamówienia oraz obiektów Q do wyszukiwarki.
4. **Użytkownicy:** Rejestracja, logowanie, historia zamówień widoczna tylko dla właściciela konta.
5. **Walidacja:** Zabezpieczenie przed ujemnymi cenami i stanami magazynowymi.

## Instrukcja uruchomienia

### 1. Wymagania wstępne
Upewnij się, że masz zainstalowany Python oraz uruchomiony serwer MySQL (np. przez XAMPP).

### 2. Instalacja zależności
```bash
pip install django mysqlclient

3. Konfiguracja Bazy Danych
W pliku settings.py skonfigurowano bazę MySQL. Upewnij się, że w XAMPP utworzyłeś pustą bazę o nazwie sklep_db (lub takiej jak w Twoim settings.py).

4. Migracje i Uruchomienie
W terminalu w katalogu projektu wykonaj:

Bash

# Tworzenie tabel
python manage.py migrate


# Utworzenie administratora (do panelu /admin)
python manage.py createsuperuser

# Uruchomienie serwera
python manage.py runserver
Aplikacja będzie dostępna pod adresem: http://127.0.0.1:8000/
