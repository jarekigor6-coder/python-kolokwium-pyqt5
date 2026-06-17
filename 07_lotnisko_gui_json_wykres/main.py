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
    QMessageBox,
    QComboBox
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Lot:
    def __init__(self, numer_lotu, linia_lotnicza, kierunek, typ_operacji,
                 planowana_godzina, opoznienie_min, status):
        self.numer_lotu = numer_lotu
        self.linia_lotnicza = linia_lotnicza
        self.kierunek = kierunek
        self.typ_operacji = typ_operacji
        self.planowana_godzina = planowana_godzina
        self.opoznienie_min = opoznienie_min
        self.status = status


class LotniskoManager:
    def __init__(self):
        self.loty = []

    def dodaj_lot(self, lot):
        self.loty.append(lot)

    def znajdz_lot(self, numer_lotu):
        for lot in self.loty:
            if lot.numer_lotu == numer_lotu:
                return lot
        return None

    def aktualizuj_lot(self, numer_lotu, nowe_opoznienie, nowy_status):
        lot = self.znajdz_lot(numer_lotu)

        if lot is not None:
            lot.opoznienie_min = nowe_opoznienie
            lot.status = nowy_status
            return True

        return False

    def srednie_opoznienie_per_linia(self):
        suma_opoznien = {}
        liczba_lotow = {}

        for lot in self.loty:
            linia = lot.linia_lotnicza

            if linia not in suma_opoznien:
                suma_opoznien[linia] = 0
                liczba_lotow[linia] = 0

            suma_opoznien[linia] += lot.opoznienie_min
            liczba_lotow[linia] += 1

        srednie = {}

        for linia in suma_opoznien:
            srednie[linia] = suma_opoznien[linia] / liczba_lotow[linia]

        return srednie

    def zapisz_json(self, sciezka):
        dane = []

        for lot in self.loty:
            dane.append(lot.__dict__)

        with open(sciezka, "w", encoding="utf-8") as plik:
            json.dump(dane, plik, ensure_ascii=False, indent=4)

    def wczytaj_json(self, sciezka):
        with open(sciezka, "r", encoding="utf-8") as plik:
            dane = json.load(plik)

        self.loty = []

        for element in dane:
            lot = Lot(**element)
            self.loty.append(lot)

    def wyczysc_dane(self):
        self.loty.clear()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.manager = LotniskoManager()

        self.setWindowTitle("Panel lotniska")
        self.setGeometry(200, 200, 1100, 750)

        self.utworz_interfejs()

    def utworz_interfejs(self):
        glowny_widget = QWidget()
        glowny_layout = QVBoxLayout()

        formularz_layout = QHBoxLayout()

        self.input_numer = QLineEdit()
        self.input_linia = QLineEdit()
        self.input_kierunek = QLineEdit()
        self.input_godzina = QLineEdit()
        self.input_opoznienie = QLineEdit()

        self.combo_typ = QComboBox()
        self.combo_typ.addItems(["Przylot", "Wylot"])

        self.combo_status = QComboBox()
        self.combo_status.addItems([
            "Planowany",
            "Boarding",
            "Opóźniony",
            "Odwołany",
            "Wykonany"
        ])

        self.input_numer.setPlaceholderText("Numer lotu")
        self.input_linia.setPlaceholderText("Linia lotnicza")
        self.input_kierunek.setPlaceholderText("Kierunek")
        self.input_godzina.setPlaceholderText("Godzina")
        self.input_opoznienie.setPlaceholderText("Opóźnienie [min]")

        formularz_layout.addWidget(QLabel("Numer:"))
        formularz_layout.addWidget(self.input_numer)

        formularz_layout.addWidget(QLabel("Linia:"))
        formularz_layout.addWidget(self.input_linia)

        formularz_layout.addWidget(QLabel("Kierunek:"))
        formularz_layout.addWidget(self.input_kierunek)

        formularz_layout.addWidget(QLabel("Typ:"))
        formularz_layout.addWidget(self.combo_typ)

        formularz_layout.addWidget(QLabel("Godzina:"))
        formularz_layout.addWidget(self.input_godzina)

        formularz_layout.addWidget(QLabel("Opóźnienie:"))
        formularz_layout.addWidget(self.input_opoznienie)

        formularz_layout.addWidget(QLabel("Status:"))
        formularz_layout.addWidget(self.combo_status)

        przyciski_layout = QHBoxLayout()

        self.przycisk_dodaj = QPushButton("Dodaj lot")
        self.przycisk_aktualizuj = QPushButton("Aktualizuj lot")
        self.przycisk_zapisz = QPushButton("Zapisz JSON")
        self.przycisk_wczytaj = QPushButton("Wczytaj JSON")
        self.przycisk_wyczysc = QPushButton("Wyczyść dane")
        self.przycisk_wykres = QPushButton("Odśwież wykres")

        self.przycisk_dodaj.clicked.connect(self.dodaj_lot_z_formularza)
        self.przycisk_aktualizuj.clicked.connect(self.aktualizuj_lot_z_formularza)
        self.przycisk_zapisz.clicked.connect(self.zapisz_json)
        self.przycisk_wczytaj.clicked.connect(self.wczytaj_json)
        self.przycisk_wyczysc.clicked.connect(self.wyczysc_dane)
        self.przycisk_wykres.clicked.connect(self.rysuj_wykres)

        przyciski_layout.addWidget(self.przycisk_dodaj)
        przyciski_layout.addWidget(self.przycisk_aktualizuj)
        przyciski_layout.addWidget(self.przycisk_zapisz)
        przyciski_layout.addWidget(self.przycisk_wczytaj)
        przyciski_layout.addWidget(self.przycisk_wyczysc)
        przyciski_layout.addWidget(self.przycisk_wykres)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(7)
        self.tabela.setHorizontalHeaderLabels([
            "Numer lotu",
            "Linia",
            "Kierunek",
            "Typ operacji",
            "Godzina",
            "Opóźnienie [min]",
            "Status"
        ])

        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)

        glowny_layout.addLayout(formularz_layout)
        glowny_layout.addLayout(przyciski_layout)
        glowny_layout.addWidget(self.tabela)
        glowny_layout.addWidget(self.canvas)

        glowny_widget.setLayout(glowny_layout)
        self.setCentralWidget(glowny_widget)

    def dodaj_lot_z_formularza(self):
        try:
            numer_lotu = self.input_numer.text()
            linia = self.input_linia.text()
            kierunek = self.input_kierunek.text()
            typ_operacji = self.combo_typ.currentText()
            godzina = self.input_godzina.text()
            opoznienie = int(self.input_opoznienie.text())
            status = self.combo_status.currentText()

            if numer_lotu == "" or linia == "":
                QMessageBox.warning(self, "Błąd", "Numer lotu i linia lotnicza nie mogą być puste.")
                return

            lot = Lot(
                numer_lotu,
                linia,
                kierunek,
                typ_operacji,
                godzina,
                opoznienie,
                status
            )

            self.manager.dodaj_lot(lot)

            self.odswiez_tabele()
            self.rysuj_wykres()
            self.wyczysc_formularz()

        except ValueError:
            QMessageBox.warning(self, "Błąd", "Opóźnienie musi być liczbą całkowitą.")

    def aktualizuj_lot_z_formularza(self):
        try:
            numer_lotu = self.input_numer.text()
            nowe_opoznienie = int(self.input_opoznienie.text())
            nowy_status = self.combo_status.currentText()

            sukces = self.manager.aktualizuj_lot(
                numer_lotu,
                nowe_opoznienie,
                nowy_status
            )

            if sukces:
                self.odswiez_tabele()
                self.rysuj_wykres()
                QMessageBox.information(self, "Zaktualizowano", "Dane lotu zostały zmienione.")
            else:
                QMessageBox.warning(self, "Błąd", "Nie znaleziono lotu o podanym numerze.")

        except ValueError:
            QMessageBox.warning(self, "Błąd", "Opóźnienie musi być liczbą całkowitą.")

    def odswiez_tabele(self):
        self.tabela.setRowCount(0)

        for lot in self.manager.loty:
            row = self.tabela.rowCount()
            self.tabela.insertRow(row)

            self.tabela.setItem(row, 0, QTableWidgetItem(lot.numer_lotu))
            self.tabela.setItem(row, 1, QTableWidgetItem(lot.linia_lotnicza))
            self.tabela.setItem(row, 2, QTableWidgetItem(lot.kierunek))
            self.tabela.setItem(row, 3, QTableWidgetItem(lot.typ_operacji))
            self.tabela.setItem(row, 4, QTableWidgetItem(lot.planowana_godzina))
            self.tabela.setItem(row, 5, QTableWidgetItem(str(lot.opoznienie_min)))
            self.tabela.setItem(row, 6, QTableWidgetItem(lot.status))

    def rysuj_wykres(self):
        dane = self.manager.srednie_opoznienie_per_linia()

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if len(dane) == 0:
            ax.set_title("Brak danych do wykresu")
            ax.text(
                0.5,
                0.5,
                "Dodaj loty, aby zobaczyć średnie opóźnienia",
                ha="center",
                va="center"
            )
        else:
            ax.bar(dane.keys(), dane.values())
            ax.set_title("Średnie opóźnienie według linii lotniczej")
            ax.set_xlabel("Linia lotnicza")
            ax.set_ylabel("Średnie opóźnienie [min]")

        self.canvas.draw()

    def wyczysc_formularz(self):
        self.input_numer.clear()
        self.input_linia.clear()
        self.input_kierunek.clear()
        self.input_godzina.clear()
        self.input_opoznienie.clear()

    def wyczysc_dane(self):
        self.manager.wyczysc_dane()
        self.odswiez_tabele()
        self.rysuj_wykres()

    def zapisz_json(self):
        sciezka, _ = QFileDialog.getSaveFileName(
            self,
            "Zapisz plik JSON",
            "",
            "Pliki JSON (*.json)"
        )

        if sciezka:
            self.manager.zapisz_json(sciezka)
            QMessageBox.information(self, "Zapisano", "Dane zapisano do pliku JSON.")

    def wczytaj_json(self):
        sciezka, _ = QFileDialog.getOpenFileName(
            self,
            "Wczytaj plik JSON",
            "",
            "Pliki JSON (*.json)"
        )

        if sciezka:
            self.manager.wczytaj_json(sciezka)
            self.odswiez_tabele()
            self.rysuj_wykres()
            QMessageBox.information(self, "Wczytano", "Dane wczytano z pliku JSON.")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
