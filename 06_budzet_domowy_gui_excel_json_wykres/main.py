import sys
import json
import pandas as pd

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


class Wydatek:
    def __init__(self, data, kategoria, kwota, opis):
        self.data = data
        self.kategoria = kategoria
        self.kwota = kwota
        self.opis = opis


class BudgetManager:
    def __init__(self):
        self.wydatki = []

    def dodaj_wydatek(self, wydatek):
        self.wydatki.append(wydatek)

    def czysc_dane(self):
        self.wydatki.clear()

    def oblicz_sume_kategorii(self):
        suma = {}

        for wydatek in self.wydatki:
            kategoria = wydatek.kategoria

            if kategoria not in suma:
                suma[kategoria] = 0

            suma[kategoria] += wydatek.kwota

        return suma

    def wczytaj_z_excela(self, sciezka):
        df = pd.read_excel(sciezka)

        wymagane_kolumny = ["Data", "Kategoria", "Kwota", "Opis"]

        for kolumna in wymagane_kolumny:
            if kolumna not in df.columns:
                raise ValueError(f"Brakuje kolumny: {kolumna}")

        self.wydatki = []

        for _, row in df.iterrows():
            wydatek = Wydatek(
                str(row["Data"]),
                str(row["Kategoria"]),
                float(row["Kwota"]),
                str(row["Opis"])
            )
            self.wydatki.append(wydatek)

    def eksport_do_excela(self, sciezka):
        dane = []

        for wydatek in self.wydatki:
            dane.append({
                "Data": wydatek.data,
                "Kategoria": wydatek.kategoria,
                "Kwota": wydatek.kwota,
                "Opis": wydatek.opis
            })

        df = pd.DataFrame(dane)
        df.to_excel(sciezka, index=False)

    def zapisz_json(self, sciezka):
        dane = []

        for wydatek in self.wydatki:
            dane.append(wydatek.__dict__)

        with open(sciezka, "w", encoding="utf-8") as plik:
            json.dump(dane, plik, ensure_ascii=False, indent=4)

    def wczytaj_json(self, sciezka):
        with open(sciezka, "r", encoding="utf-8") as plik:
            dane = json.load(plik)

        self.wydatki = []

        for element in dane:
            wydatek = Wydatek(**element)
            self.wydatki.append(wydatek)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.manager = BudgetManager()

        self.setWindowTitle("Budżet domowy")
        self.setGeometry(200, 200, 1000, 700)

        self.utworz_interfejs()

    def utworz_interfejs(self):
        glowny_widget = QWidget()
        glowny_layout = QVBoxLayout()

        formularz_layout = QHBoxLayout()

        self.input_data = QLineEdit()
        self.input_kategoria = QLineEdit()
        self.input_kwota = QLineEdit()
        self.input_opis = QLineEdit()

        self.input_data.setPlaceholderText("Data")
        self.input_kategoria.setPlaceholderText("Kategoria")
        self.input_kwota.setPlaceholderText("Kwota")
        self.input_opis.setPlaceholderText("Opis")

        formularz_layout.addWidget(QLabel("Data:"))
        formularz_layout.addWidget(self.input_data)

        formularz_layout.addWidget(QLabel("Kategoria:"))
        formularz_layout.addWidget(self.input_kategoria)

        formularz_layout.addWidget(QLabel("Kwota:"))
        formularz_layout.addWidget(self.input_kwota)

        formularz_layout.addWidget(QLabel("Opis:"))
        formularz_layout.addWidget(self.input_opis)

        przyciski_layout = QHBoxLayout()

        self.przycisk_dodaj = QPushButton("Dodaj wydatek")
        self.przycisk_excel = QPushButton("Wczytaj Excel")
        self.przycisk_eksport = QPushButton("Eksport Excel")
        self.przycisk_zapisz_json = QPushButton("Zapisz JSON")
        self.przycisk_wczytaj_json = QPushButton("Wczytaj JSON")
        self.przycisk_wyczysc = QPushButton("Wyczyść dane")
        self.przycisk_wykres = QPushButton("Odśwież wykres")

        self.przycisk_dodaj.clicked.connect(self.dodaj_wydatek_z_formularza)
        self.przycisk_excel.clicked.connect(self.wczytaj_excel)
        self.przycisk_eksport.clicked.connect(self.eksport_excel)
        self.przycisk_zapisz_json.clicked.connect(self.zapisz_json)
        self.przycisk_wczytaj_json.clicked.connect(self.wczytaj_json)
        self.przycisk_wyczysc.clicked.connect(self.wyczysc_dane)
        self.przycisk_wykres.clicked.connect(self.rysuj_wykres)

        przyciski_layout.addWidget(self.przycisk_dodaj)
        przyciski_layout.addWidget(self.przycisk_excel)
        przyciski_layout.addWidget(self.przycisk_eksport)
        przyciski_layout.addWidget(self.przycisk_zapisz_json)
        przyciski_layout.addWidget(self.przycisk_wczytaj_json)
        przyciski_layout.addWidget(self.przycisk_wyczysc)
        przyciski_layout.addWidget(self.przycisk_wykres)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(4)
        self.tabela.setHorizontalHeaderLabels([
            "Data",
            "Kategoria",
            "Kwota",
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

    def dodaj_wydatek_z_formularza(self):
        try:
            data = self.input_data.text()
            kategoria = self.input_kategoria.text()
            kwota = float(self.input_kwota.text().replace(",", "."))
            opis = self.input_opis.text()

            wydatek = Wydatek(data, kategoria, kwota, opis)

            self.manager.dodaj_wydatek(wydatek)

            self.odswiez_tabele()
            self.rysuj_wykres()
            self.wyczysc_formularz()

        except ValueError:
            QMessageBox.warning(self, "Błąd", "Kwota musi być liczbą.")

    def odswiez_tabele(self):
        self.tabela.setRowCount(0)

        for wydatek in self.manager.wydatki:
            row = self.tabela.rowCount()
            self.tabela.insertRow(row)

            self.tabela.setItem(row, 0, QTableWidgetItem(wydatek.data))
            self.tabela.setItem(row, 1, QTableWidgetItem(wydatek.kategoria))
            self.tabela.setItem(row, 2, QTableWidgetItem(str(wydatek.kwota)))
            self.tabela.setItem(row, 3, QTableWidgetItem(wydatek.opis))

    def rysuj_wykres(self):
        dane = self.manager.oblicz_sume_kategorii()

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if len(dane) == 0:
            ax.set_title("Brak danych do wykresu")
            ax.text(
                0.5,
                0.5,
                "Dodaj wydatki albo wczytaj plik Excel",
                ha="center",
                va="center"
            )
        else:
            ax.bar(dane.keys(), dane.values())
            ax.set_title("Suma wydatków według kategorii")
            ax.set_xlabel("Kategoria")
            ax.set_ylabel("Kwota [zł]")

        self.canvas.draw()

    def wyczysc_formularz(self):
        self.input_data.clear()
        self.input_kategoria.clear()
        self.input_kwota.clear()
        self.input_opis.clear()

    def wyczysc_dane(self):
        self.manager.czysc_dane()
        self.odswiez_tabele()
        self.rysuj_wykres()

    def wczytaj_excel(self):
        sciezka, _ = QFileDialog.getOpenFileName(
            self,
            "Wczytaj plik Excel",
            "",
            "Pliki Excel (*.xlsx)"
        )

        if sciezka:
            try:
                self.manager.wczytaj_z_excela(sciezka)
                self.odswiez_tabele()
                self.rysuj_wykres()
                QMessageBox.information(self, "Wczytano", "Dane wczytano z pliku Excel.")
            except Exception as blad:
                QMessageBox.warning(self, "Błąd", str(blad))

    def eksport_excel(self):
        sciezka, _ = QFileDialog.getSaveFileName(
            self,
            "Zapisz plik Excel",
            "",
            "Pliki Excel (*.xlsx)"
        )

        if sciezka:
            self.manager.eksport_do_excela(sciezka)
            QMessageBox.information(self, "Zapisano", "Dane zapisano do pliku Excel.")

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
