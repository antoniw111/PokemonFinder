from pathlib import Path
import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class AssetManager:
    def __init__(self, cache_folder_name="cache"):
        self.working_dir = Path.cwd()
        self.cache_dir = self.working_dir / cache_folder_name
        self._ensure_cache_exists()
        self.pokemon_data = None

    def _ensure_cache_exists(self):
        try:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            print(f"Cache directory ready at: {self.cache_dir}")
        except OSError as e:
            print(f"Critical Error: Could not create cache. {e}")

    def get_pokemon(self, pokemon):
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
        try:
            response = requests.get(url)
            response.raise_for_status()

            self.pokemon_data = response.json()
            pic_url = self.pokemon_data["sprites"]["other"]["official-artwork"]["front_default"]
            pokemon = self.pokemon_data["forms"][0]["name"].capitalize()
            print(pokemon.capitalize())
            return self.get_image(pic_url, f"{pokemon}.png"), pokemon
        except requests.RequestException as e:
            print(f"Network error: {e}")
            return None, None

    def get_image(self, url, filename):
        target_path = self.cache_dir / filename

        if target_path.exists():
            print(f"Loaded from cache: {filename}")
            return str(target_path)

        print(f"Downloading {filename} from web...")
        success = self._download_file(url, target_path)

        if success:
            return str(target_path)
        else:
            return self.get_placeholder()

    def get_placeholder(self):
        placeholder_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/132.png"
        return self.get_image(placeholder_url, "placeholder.png")

    @staticmethod
    def _download_file(url, target_path):

        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(target_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print("Download complete.")
            return str(target_path)
        except requests.RequestException as e:
            print(f"Network error: {e}")
            return None

class PokemonFinder(QWidget):
    def __init__(self, asset_manager):
        super().__init__()
        self.title = QLabel("Enter Pokemon name: ", self)
        self.pokemon_input = QLineEdit(self)
        self.get_pokemon_button = QPushButton("Look for Pokemon", self)
        self.pokemon_label = QLabel("Ditto", self)
        self.pokemon_pic = QLabel(self)
        self.asset_manager = asset_manager
        self.current_img_path = self.asset_manager.get_placeholder()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Pokemon Finder")
        pixmap = QPixmap(self.current_img_path)
        self.pokemon_pic.setPixmap(pixmap)

        self.get_pokemon_button.clicked.connect(self.update_pokemon)

        vbox = QVBoxLayout()
        vbox.addWidget(self.title)
        vbox.addWidget(self.pokemon_input)
        vbox.addWidget(self.get_pokemon_button)
        vbox.addWidget(self.pokemon_pic)
        vbox.addWidget(self.pokemon_label)

        self.setLayout(vbox)

        self.title.setAlignment(Qt.AlignCenter)
        self.pokemon_input.setAlignment(Qt.AlignCenter)
        self.pokemon_label.setAlignment(Qt.AlignCenter)
        self.pokemon_pic.setAlignment(Qt.AlignCenter)

        self.title.setObjectName("title")
        self.pokemon_input.setObjectName("pokemon_input")
        self.get_pokemon_button.setObjectName("get_pokemon_button")
        self.pokemon_label.setObjectName("pokemon_label")
        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: "Segoe UI", sans-serif;
            }
            QLabel#title{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#pokemon_input{
                font-size: 40px;
                padding: 5px;
            }
            QPushButton#get_pokemon_button{
                font-size: 30px;
                font-weight: bold;
                background-color: #ddd;
            }
            QLabel#pokemon_label{
                font-size: 50px;
            }
        """)

    def update_pokemon(self):
        pokemon = self.pokemon_input.text()
        self.current_img_path, pokemon = self.asset_manager.get_pokemon(pokemon)
        pixmap = QPixmap(self.current_img_path)
        self.pokemon_pic.setPixmap(pixmap)
        if self.current_img_path is None:
            self.pokemon_label.setText("Pokemon had not been found!")
        else:
            self.pokemon_label.setText(pokemon.capitalize())



if __name__ == "__main__":

    assets = AssetManager()
    app = QApplication(sys.argv)
    pokemon_finder = PokemonFinder(assets)
    pokemon_finder.show()
    sys.exit(app.exec_())
