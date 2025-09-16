import sys

import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt
from requests import HTTPError, RequestException, TooManyRedirects, Timeout


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle("Weather App")
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        vbox.setSpacing(20)
        vbox.setContentsMargins(20, 20, 20, 20)

        # Set fixed height for QLineEdit
        self.city_input.setFixedHeight(60)
        self.city_input.setMinimumWidth(300)

        self.setLayout(vbox)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label{
                font-size: 75px;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: "Apple Color Emoji";
            }
            QLabel#description_label{
                font-size: 50px;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "03e36f18f5537a432c0bf77cda0daaf8"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)
        # except HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAcess is denied")
                case 404:
                    self.display_error("Not found:\nCIty not find")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")

        except ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")
        except Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        except TooManyRedirects:
            self.display_error("Too many Redirects:\nThe request timed out")
        except RequestException:
            self.display_error("RequestException:\nRequestException")

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        weather_description = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]
        weather_emoji = self.get_weather_emoji(weather_id)

        self.temperature_label.setText(f"{temperature_c:.1f} ℃")
        self.description_label.setText(weather_description)
        self.emoji_label.setText(weather_emoji)

    @staticmethod
    def get_weather_emoji(weather_id):
        match weather_id:
            case 200 | 201 | 202 | 210 | 211 | 212 | 221 | 230 | 231 | 232:
                return "⚡"  # thunderstorm
            case 300 | 301 | 302 | 310 | 311 | 312 | 313 | 314 | 321:
                return "🌧️"  # drizzle
            case 500 | 501 | 502 | 503 | 504 | 511 | 520 | 521 | 522 | 531:
                return "🌧️"  # rain
            case 600 | 601 | 602 | 611 | 612 | 613 | 615 | 616 | 620 | 621 | 622:
                return "❄️"  # snow
            case 701 | 711 | 721 | 731 | 741 | 751 | 761 | 762 | 771 | 781:
                return "🌫️"  # atmosphere
            case 800:
                return "☀️"  # clear sky
            case 801 | 802 | 803 | 804:
                return "☁️"  # clouds
            case _:
                return "❓"  # unknown



if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())