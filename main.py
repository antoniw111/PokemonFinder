import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

class PokemonFinder(QWidget):
    def __init__(self):
        super().__init__()
        self.pokemon_name = QLabel("Enter Pokemon name: ", self)
        self.pokemon_input = QLineEdit(self)
        self.get_pokemon_button = QPushButton("Look for Pokemon", self)
        self.pokemon_label = QLabel("Charmander", self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Pokemon Finder")

        vbox = QVBoxLayout()
        vbox.addWidget(self.pokemon_name)
        vbox.addWidget(self.pokemon_input)
        vbox.addWidget(self.get_pokemon_button)
        vbox.addWidget(self.pokemon_label)

        self.setLayout(vbox)

        self.pokemon_name.setAlignment(Qt.AlignCenter)
        self.pokemon_input.setAlignment(Qt.AlignCenter)
        self.pokemon_label.setAlignment(Qt.AlignCenter)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pokemon_finder = PokemonFinder()
    pokemon_finder.show()
    sys.exit(app.exec_())