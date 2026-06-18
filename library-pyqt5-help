import sys
import json

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem,
    QFileDialog, QMessageBox
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Rekord:
    def __init__(self, nazwa, kategoria, wartosc, opis):
        self.nazwa = nazwa
        self.kategoria = kategoria
        self.wartosc = wartosc
        self.opis = opis


class Manager:
    def __init__(self):
        self.rekordy = []

    def dodaj_rekord(self, rekord):
        self.rekordy.append(rekord)

    def czysc_dane(self):
        self.rekordy.clear()

    def suma_wedlug_kategorii(self):
        wynik = {}

        for rekord in self.rekordy:
            kategoria = rekord.kategoria

            if kategoria not in wynik:
                wynik[kategoria] = 0

            wynik[kategoria] += rekord.wartosc

        return wynik

    def zapisz_json(self, sciezka):
        dane = []

        for rekord in self.rekordy:
            dane.append(rekord.__dict__)

        with open(sciezka, "w", encoding="utf-8") as plik:
            json.dump(dane, plik, ensure_ascii=False, indent=4)

    def wczytaj_json(self, sciezka):
        with open(sciezka, "r", encoding="utf-8") as plik:
            dane = json.load(plik)

        self.rekordy = []

        for element in dane:
            rekord = Rekord(**element)
            self.rekordy.append(rekord)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.manager = Manager()

        self.setWindowTitle("Szablon uniwersalny")
        self.setGeometry(200, 200, 1000, 700)

        self.utworz_interfejs()

    def utworz_interfejs(self):
        glowny_widget = QWidget()
        glowny_layout = QVBoxLayout()

        formularz_layout = QHBoxLayout()

        self.input_nazwa = QLineEdit()
        self.input_kategoria = QLineEdit()
        self.input_wartosc = QLineEdit()
        self.input_opis = QLineEdit()

        self.input_nazwa.setPlaceholderText("Nazwa")
        self.input_kategoria.setPlaceholderText("Kategoria")
        self.input_wartosc.setPlaceholderText("Wartość")
        self.input_opis.setPlaceholderText("Opis")

        formularz_layout.addWidget(QLabel("Nazwa:"))
        formularz_layout.addWidget(self.input_nazwa)

        formularz_layout.addWidget(QLabel("Kategoria:"))
        formularz_layout.addWidget(self.input_kategoria)

        formularz_layout.addWidget(QLabel("Wartość:"))
        formularz_layout.addWidget(self.input_wartosc)

        formularz_layout.addWidget(QLabel("Opis:"))
        formularz_layout.addWidget(self.input_opis)

        przyciski_layout = QHBoxLayout()

        self.przycisk_dodaj = QPushButton("Dodaj rekord")
        self.przycisk_zapisz = QPushButton("Zapisz JSON")
        self.przycisk_wczytaj = QPushButton("Wczytaj JSON")
        self.przycisk_wyczysc = QPushButton("Wyczyść dane")
        self.przycisk_wykres = QPushButton("Odśwież wykres")

        self.przycisk_dodaj.clicked.connect(self.dodaj_rekord_z_formularza)
        self.przycisk_zapisz.clicked.connect(self.zapisz_json)
        self.przycisk_wczytaj.clicked.connect(self.wczytaj_json)
        self.przycisk_wyczysc.clicked.connect(self.wyczysc_dane)
        self.przycisk_wykres.clicked.connect(self.rysuj_wykres)

        przyciski_layout.addWidget(self.przycisk_dodaj)
        przyciski_layout.addWidget(self.przycisk_zapisz)
        przyciski_layout.addWidget(self.przycisk_wczytaj)
        przyciski_layout.addWidget(self.przycisk_wyczysc)
        przyciski_layout.addWidget(self.przycisk_wykres)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(4)
        self.tabela.setHorizontalHeaderLabels([
            "Nazwa",
            "Kategoria",
            "Wartość",
            "Opis"
        ])

        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)

        glowny_layout.addLayout(formularz_layout)
        glowny_layout.addLayout(przyciski_layout)
        glowny_layout.addWidget(self.tabela)
        glowny_layout.addWidget(self.canvas)

        glowny_widget.setLayout(glowny_layout)
        self.setCentralWidget(glowny_widget)

    def dodaj_rekord_z_formularza(self):
        try:
            nazwa = self.input_nazwa.text()
            kategoria = self.input_kategoria.text()
            wartosc = float(self.input_wartosc.text().replace(",", "."))
            opis = self.input_opis.text()

            rekord = Rekord(nazwa, kategoria, wartosc, opis)

            self.manager.dodaj_rekord(rekord)

            self.odswiez_tabele()
            self.rysuj_wykres()
            self.wyczysc_formularz()

        except ValueError:
            QMessageBox.warning(self, "Błąd", "Wartość musi być liczbą.")

    def odswiez_tabele(self):
        self.tabela.setRowCount(0)

        for rekord in self.manager.rekordy:
            row = self.tabela.rowCount()
            self.tabela.insertRow(row)

            self.tabela.setItem(row, 0, QTableWidgetItem(rekord.nazwa))
            self.tabela.setItem(row, 1, QTableWidgetItem(rekord.kategoria))
            self.tabela.setItem(row, 2, QTableWidgetItem(str(rekord.wartosc)))
            self.tabela.setItem(row, 3, QTableWidgetItem(rekord.opis))

    def rysuj_wykres(self):
        dane = self.manager.suma_wedlug_kategorii()

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if len(dane) == 0:
            ax.set_title("Brak danych do wykresu")
            ax.text(
                0.5,
                0.5,
                "Dodaj rekordy, aby zobaczyć wykres",
                ha="center",
                va="center"
            )
        else:
            ax.bar(dane.keys(), dane.values())
            ax.set_title("Suma wartości według kategorii")
            ax.set_xlabel("Kategoria")
            ax.set_ylabel("Wartość")

        self.canvas.draw()

    def wyczysc_formularz(self):
        self.input_nazwa.clear()
        self.input_kategoria.clear()
        self.input_wartosc.clear()
        self.input_opis.clear()

    def wyczysc_dane(self):
        self.manager.czysc_dane()
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
            QMessageBox.information(self, "Zapisano", "Dane zapisano do JSON.")

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
            QMessageBox.information(self, "Wczytano", "Dane wczytano z JSON.")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
