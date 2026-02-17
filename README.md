# Sklep Internetowy Django

Projekt sklepu internetowego stworzony w ramach zaliczenia kursu. Aplikacja umożliwia przeglądanie produktów, dodawanie ich do koszyka, składanie zamówień oraz przeglądanie historii zakupów przez zalogowanych użytkowników.

## Technologie
* Python 3.13
* Django 5.0.4
* Sqlite
* HTML5 / CSS3

## Funkcjonalności (Kryteria oceny)
1. **Architektura MVT:** Podział na modele, widoki i szablony.
2. **Modele:** Relacje ForeignKey (Kategorie, Zamówienia) oraz ManyToMany (Tagi).
3. **ORM:** Wykorzystanie agregacji (Sum) do obliczania wartości zamówienia oraz obiektów Q do wyszukiwarki.
4. **Użytkownicy:** Rejestracja, logowanie, historia zamówień widoczna tylko dla właściciela konta.
5. **Walidacja:** Zabezpieczenie przed ujemnymi cenami i stanami magazynowymi.

## Panel Admina

Panel admina jest dostepny pod loginem 'admin' 
Haslo 'admin'
http://127.0.0.1:8000/admin