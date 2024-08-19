from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
import os
from pickle import dump, load

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Create layout
        self.main_layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        # Create widgets
        self.mv = QLineEdit()
        self.nv = QLineEdit()
        self.p = QLineEdit()

        self.form_layout.addRow(QLabel("Matricule:"), self.mv)
        self.form_layout.addRow(QLabel("Modèle:"), self.nv)
        self.form_layout.addRow(QLabel("Prix:"), self.p)

        self.aj = QPushButton("Ajouter")
        self.af = QPushButton("Afficher")

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Matricule", "Modèle", "Prix"])

        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.aj)
        self.main_layout.addWidget(self.af)
        self.main_layout.addWidget(self.table_widget)

        self.setLayout(self.main_layout)
        self.setWindowTitle("Agence de location")

        # Connect buttons to functions
        self.aj.clicked.connect(self.ajouter)
        self.af.clicked.connect(self.affiche)

    def verif_mat(self, ch):
        pt = ch.find("T")
        if pt == -1:
            return False
        ns = ch[:pt]
        p = ch[pt:pt+3]
        nv = ch[pt+3:]
        if p.upper() == "TUN" and nv.isdigit() and int(nv) in range(1, 10000) and ns.isdigit() and int(ns) in range(1, 246):
            return True
        return False

    def ajouter(self):
        mat = self.mv.text()
        nv = self.nv.text()
        prix = self.p.text()
        if mat == "" or nv == "" or prix == "":
            QMessageBox.critical(self, "ATTENTION", "REMPLIRE TOUT LES CHAMPS !!")
        elif not self.verif_mat(mat):
            QMessageBox.critical(self, "ATTENTION", "VERIFIE LA MATRICULE DE VOITURE !!")
        elif not prix.isdecimal():
            QMessageBox.critical(self, "ATTENTION", "VERIFIE LE PRIX DE LOCATION !!")
        else:
            try:
                prix_int = int(prix)
                e = {"m": mat, "n": nv, "p": prix_int}
                with open("stock.dat", "ab") as f:
                    dump(e, f)
                QMessageBox.information(self, "Félicitations", "Voiture ajoutée !!")
            except Exception as ex:
                QMessageBox.critical(self, "Erreur", f"Une erreur est survenue : {ex}")

    def affiche(self):
        if os.path.exists("stock.dat"):
            self.table_widget.setRowCount(0)  # Clear existing rows
            with open("stock.dat", "rb") as f:
                l = 0
                while True:
                    try:
                        e = load(f)
                        self.table_widget.insertRow(l)
                        self.table_widget.setItem(l, 0, QTableWidgetItem(e["m"]))
                        self.table_widget.setItem(l, 1, QTableWidgetItem(e["n"]))
                        self.table_widget.setItem(l, 2, QTableWidgetItem(str(e["p"])))
                        l += 1
                    except EOFError:
                        break
        else:
            QMessageBox.warning(self, "Information", "Aucune donnée à afficher.")

        self.mv.clear()
        self.nv.clear()
        self.p.clear()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
