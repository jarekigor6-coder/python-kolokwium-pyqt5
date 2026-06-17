# Notatka startowa Python OOP

## Podstawowe słowa w Pythonie

`class` - tworzy klasę, czyli wzór obiektu.

`def` - tworzy funkcję albo metodę.

`__init__` - konstruktor. Uruchamia się automatycznie przy tworzeniu nowego obiektu.

`self` - oznacza konkretny obiekt, na którym pracujemy.

`for` - pętla, która przechodzi po elementach listy.

`if` - warunek.

`return` - zwraca wynik z funkcji.

`print` - wyświetla wynik w konsoli.

`append` - dodaje element do listy.

---

## Co oznacza klasa danych?

Przykład:

```python
class Tankowanie:
    def __init__(self, id, rejestracja, data, stan_licznika, litry_paliwa, koszt_calkowity):
        self.id = id
        self.rejestracja = rejestracja
        self.data = data
        self.stan_licznika = stan_licznika
        self.litry_paliwa = litry_paliwa
        self.koszt_calkowity = koszt_calkowity
