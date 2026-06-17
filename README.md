# Python kolokwium - schematy PyQt5 OOP

## Główny schemat każdego zadania

Każde zadanie robimy według układu:

1. Klasa danych - opisuje jeden rekord.
2. Manager - przechowuje listę rekordów i wykonuje operacje.
3. GUI - formularz, przyciski, tabela.
4. Zapis i odczyt danych - JSON albo Excel.
5. Wykres - Matplotlib osadzony w PyQt5.

---

## 1. Klasa danych

Przykład:

```python
class Wydatek:
    def __init__(self, data, kategoria, kwota, opis):
        self.data = data
        self.kategoria = kategoria
        self.kwota = kwota
        self.opis = opis
