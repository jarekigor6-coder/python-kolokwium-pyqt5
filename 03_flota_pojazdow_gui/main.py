import sys

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
    QTableWidgetItem
)


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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.manager = FlotaManager()
        self.nastepne_id = 1

        self.setWindowTitle("Panel Managera Floty Pojazdów")
        self.setGeometry(200, 200, 900, 500)

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

        self.przycisk_dodaj = QPushButton("Dodaj tankowanie")
        self.przycisk_dodaj.clicked.connect(self.dodaj_tankowanie_z_formularza)

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

        glowny_layout.addLayout(formularz_layout)
        glowny_layout.addWidget(self.przycisk_dodaj)
        glowny_layout.addWidget(self.tabela)

        glowny_widget.setLayout(glowny_layout)
        self.setCentralWidget(glowny_widget)

    def dodaj_tankowanie_z_formularza(self):
        rejestracja = self.input_rejestracja.text()
        data = self.input_data.text()
        stan_licznika = int(self.input_licznik.text())
        litry_paliwa = float(self.input_litry.text())
        koszt_calkowity = float(self.input_koszt.text())

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
        self.wyczysc_formularz()

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

    def wyczysc_formularz(self):
        self.input_rejestracja.clear()
        self.input_data.clear()
        self.input_licznik.clear()
        self.input_litry.clear()
        self.input_koszt.clear()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
