import sys
import json

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QFileDialog,
    QMessageBox
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


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

    def pobierz_srednie_spalanie_wszystkich(self):
        rejestracje = set()

        for tankowanie in self.tankowania:
            rejestracje.add(tankowanie.rejestracja)

        wyniki = {}

        for rejestracja in rejestracje:
            spalanie = self.oblicz_srednie_spalanie(rejestracja)

            if spalanie is not None:
                wyniki[rejestracja] = spalanie

        return wyniki

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.manager = FlotaManager()
        self.nastepne_id = 1

        self.setWindowTitle("Panel Managera Floty Pojazdów")
        self.setGeometry(200, 200, 1000, 700)

        self.utworz_interfejs()

    def utworz_interfejs(self):
        glowny_widget = QWidget()
        glowny_layout = QVBoxLayout()

        formularz_layout = QHBoxLayout()

        self.input_rejestracja = QLineEdit()
        self.input_data = QLineEdit()
        self.input_licznik = QLineEdit()
        self.input_litry = QLineEdit()
        self.input_koszt = QLineEdit()

        self.input_rejestracja.setPlaceholderText("Rejestracja")
        self.input_data.setPlaceholderText("Data")
        self.input_licznik.setPlaceholderText("Stan licznika")
        self.input_litry.setPlaceholderText("Litry paliwa")
        self.input_koszt.setPlaceholderText("Koszt całkowity")

        formularz_layout.addWidget(QLabel("Rejestracja:"))
        formularz_layout.addWidget(self.input_rejestracja)

        formularz_layout.addWidget(QLabel("Data:"))
        formularz_layout.addWidget(self.input_data)

        formularz_layout.addWidget(QLabel("Licznik:"))
        formularz_layout.addWidget(self.input_licznik)

        formularz_layout.addWidget(QLabel("Litry:"))
        formularz_layout.addWidget(self.input_litry)

        formularz_layout.addWidget(QLabel("Koszt:"))
        formularz_layout.addWidget(self.input_koszt)

        przyciski_layout = QHBoxLayout()

        self.przycisk_dodaj = QPushButton("Dodaj tankowanie")
        self.przycisk_zapisz = QPushButton("Zapisz JSON")
        self.przycisk_wczytaj = QPushButton("Wczytaj JSON")
        self.przycisk_wykres = QPushButton("Odśwież wykres")

        self.przycisk_dodaj.clicked.connect(self.dodaj_tankowanie_z_formularza)
        self.przycisk_zapisz.clicked.connect(self.zapisz_json)
        self.przycisk_wczytaj.clicked.connect(self.wczytaj_json)
        self.przycisk_wykres.clicked.connect(self.rysuj_wykres)

        przyciski_layout.addWidget(self.przycisk_dodaj)
        przyciski_layout.addWidget(self.przycisk_zapisz)
        przyciski_layout.addWidget(self.przycisk_wczytaj)
        przyciski_layout.addWidget(self.przycisk_wykres)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels([
            "ID",
            "Rejestracja",
            "Data",
            "Stan licznika",
            "Litry paliwa",
            "Koszt całkowity"
        ])

        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)

        glowny_layout.addLayout(formularz_layout)
        glowny_layout.addLayout(przyciski_layout)
        glowny_layout.addWidget(self.tabela)
        glowny_layout.addWidget(self.canvas)

        glowny_widget.setLayout(glowny_layout)
        self.setCentralWidget(glowny_widget)

    def dodaj_tankowanie_z_formularza(self):
        try:
            rejestracja = self.input_rejestracja.text()
            data = self.input_data.text()

            stan_licznika = int(self.input_licznik.text())

            litry_paliwa = float(self.input_litry.text().replace(",", "."))
            koszt_calkowity = float(self.input_koszt.text().replace(",", "."))

            tankowanie = Tankowanie(
                self.nastepne_id,
                rejestracja,
                data,
                stan_licznika,
                litry_paliwa,
                koszt_calkowity
            )

            self.manager.dodaj_tankowanie(tankowanie)
            self.nastepne_id += 1

            self.odswiez_tabele()
            self.rysuj_wykres()
            self.wyczysc_formularz()

        except ValueError:
            QMessageBox.warning(self, "Błąd", "Licznik, litry i koszt muszą być liczbami.")

    def odswiez_tabele(self):
        self.tabela.setRowCount(0)

        for tankowanie in self.manager.tankowania:
            row = self.tabela.rowCount()
            self.tabela.insertRow(row)

            self.tabela.setItem(row, 0, QTableWidgetItem(str(tankowanie.id)))
            self.tabela.setItem(row, 1, QTableWidgetItem(tankowanie.rejestracja))
            self.tabela.setItem(row, 2, QTableWidgetItem(tankowanie.data))
            self.tabela.setItem(row, 3, QTableWidgetItem(str(tankowanie.stan_licznika)))
            self.tabela.setItem(row, 4, QTableWidgetItem(str(tankowanie.litry_paliwa)))
            self.tabela.setItem(row, 5, QTableWidgetItem(str(tankowanie.koszt_calkowity)))

    def rysuj_wykres(self):
        dane = self.manager.pobierz_srednie_spalanie_wszystkich()

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if len(dane) == 0:
            ax.set_title("Brak danych do wykresu")
            ax.text(0.5, 0.5, "Dodaj minimum 2 tankowania dla jednego auta",
                    ha="center", va="center")
        else:
            ax.bar(dane.keys(), dane.values())
            ax.set_title("Średnie spalanie samochodów")
            ax.set_xlabel("Numer rejestracyjny")
            ax.set_ylabel("Spalanie [l/100 km]")

        self.canvas.draw()

    def wyczysc_formularz(self):
        self.input_rejestracja.clear()
        self.input_data.clear()
        self.input_licznik.clear()
        self.input_litry.clear()
        self.input_koszt.clear()

    def zapisz_json(self):
        sciezka, _ = QFileDialog.getSaveFileName(
            self,
            "Zapisz plik JSON",
            "",
            "Pliki JSON (*.json)"
        )

        if sciezka:
            self.manager.zapisz_baze(sciezka)
            QMessageBox.information(self, "Zapisano", "Dane zapisano do pliku JSON.")

    def wczytaj_json(self):
        sciezka, _ = QFileDialog.getOpenFileName(
            self,
            "Wczytaj plik JSON",
            "",
            "Pliki JSON (*.json)"
        )

        if sciezka:
            self.manager.wczytaj_baze(sciezka)

            if self.manager.tankowania:
                self.nastepne_id = max(t.id for t in self.manager.tankowania) + 1
            else:
                self.nastepne_id = 1

            self.odswiez_tabele()
            self.rysuj_wykres()
            QMessageBox.information(self, "Wczytano", "Dane wczytano z pliku JSON.")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
