class Tankowanie:
    def __init__(self, id, rejestracja, data, stan_licznika, litry_paliwa, koszt_calkowity):
        self.id = id
        self.rejestracja = rejestracja
        self.data = data
        self.stan_licznika = stan_licznika
        self.litry_paliwa = litry_paliwa
        self.koszt_calkowity = koszt_calkowity


class FlotaManager:
    def __init__(self):
        # Lista przechowuje wszystkie tankowania
        self.tankowania = []

    def dodaj_tankowanie(self, tankowanie):
        # Dodaje jedno tankowanie do listy
        self.tankowania.append(tankowanie)

    def pobierz_koszty_per_samochod(self):
        # Słownik: rejestracja auta -> łączny koszt paliwa
        koszty = {}

        for tankowanie in self.tankowania:
            rejestracja = tankowanie.rejestracja

            if rejestracja not in koszty:
                koszty[rejestracja] = 0

            koszty[rejestracja] += tankowanie.koszt_calkowity

        return koszty


manager = FlotaManager()

t1 = Tankowanie(1, "WA12345", "2026-06-17", 150000, 45.5, 320.0)
t2 = Tankowanie(2, "WA12345", "2026-06-18", 150600, 40.0, 300.0)
t3 = Tankowanie(3, "LU54321", "2026-06-18", 90000, 35.0, 260.0)

manager.dodaj_tankowanie(t1)
manager.dodaj_tankowanie(t2)
manager.dodaj_tankowanie(t3)

print(manager.pobierz_koszty_per_samochod())
