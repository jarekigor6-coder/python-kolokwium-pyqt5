import json


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
        self.tankowania = []

    def dodaj_tankowanie(self, tankowanie):
        self.tankowania.append(tankowanie)

    def pobierz_koszty_per_samochod(self):
        koszty = {}

        for tankowanie in self.tankowania:
            rejestracja = tankowanie.rejestracja

            if rejestracja not in koszty:
                koszty[rejestracja] = 0

            koszty[rejestracja] += tankowanie.koszt_calkowity

        return koszty

    def oblicz_srednie_spalanie(self, nr_rejestracyjny):
        tankowania_auta = []

        for tankowanie in self.tankowania:
            if tankowanie.rejestracja == nr_rejestracyjny:
                tankowania_auta.append(tankowanie)

        tankowania_auta.sort(key=lambda x: x.stan_licznika)

        if len(tankowania_auta) < 2:
            return None

        pierwszy_licznik = tankowania_auta[0].stan_licznika
        ostatni_licznik = tankowania_auta[-1].stan_licznika

        przejechane_km = ostatni_licznik - pierwszy_licznik

        if przejechane_km <= 0:
            return None

        suma_litrow = 0

        for tankowanie in tankowania_auta[1:]:
            suma_litrow += tankowanie.litry_paliwa

        spalanie = (suma_litrow / przejechane_km) * 100

        return spalanie

    def zapisz_baze(self, sciezka):
        dane = []

        for tankowanie in self.tankowania:
            dane.append(tankowanie.__dict__)

        with open(sciezka, "w", encoding="utf-8") as plik:
            json.dump(dane, plik, ensure_ascii=False, indent=4)

    def wczytaj_baze(self, sciezka):
        with open(sciezka, "r", encoding="utf-8") as plik:
            dane = json.load(plik)

        self.tankowania = []

        for element in dane:
            tankowanie = Tankowanie(**element)
            self.tankowania.append(tankowanie)


manager = FlotaManager()

manager.dodaj_tankowanie(Tankowanie(1, "WA12345", "2026-06-10", 150000, 45.5, 320.0))
manager.dodaj_tankowanie(Tankowanie(2, "WA12345", "2026-06-15", 150600, 40.0, 300.0))
manager.dodaj_tankowanie(Tankowanie(3, "WA12345", "2026-06-20", 151200, 42.0, 315.0))
manager.dodaj_tankowanie(Tankowanie(4, "LU54321", "2026-06-12", 90000, 35.0, 260.0))
manager.dodaj_tankowanie(Tankowanie(5, "LU54321", "2026-06-18", 90450, 32.0, 240.0))

print("Koszty paliwa per samochód:")
print(manager.pobierz_koszty_per_samochod())

print("Średnie spalanie WA12345:")
print(manager.oblicz_srednie_spalanie("WA12345"))

manager.zapisz_baze("flota.json")

nowy_manager = FlotaManager()
nowy_manager.wczytaj_baze("flota.json")

print("Dane po odczycie z JSON:")
print(nowy_manager.pobierz_koszty_per_samochod())
