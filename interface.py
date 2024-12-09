import sys
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import QTimer

ESP8266_IP = '192.168.15.15'

class SensorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monitor de Sensores")
        self.resize(300, 200)

        self.layout = QVBoxLayout()
        self.temperature_label = QLabel("Temperatura: -- °C")
        self.humidity_label = QLabel("Umidade: -- %")
        self.gas_label = QLabel("Gás: --")
        self.refresh_button = QPushButton("Atualizar")

        self.layout.addWidget(self.temperature_label)
        self.layout.addWidget(self.humidity_label)
        self.layout.addWidget(self.gas_label)
        self.layout.addWidget(self.refresh_button)
        self.setLayout(self.layout)

        self.refresh_button.clicked.connect(self.update_data)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(2000)

    def update_data(self):
        try:
            headers = {"User-Agent": "PythonESPClient"}
            response = requests.get(f"http://{ESP8266_IP}/json", headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                self.temperature_label.setText(f"Temperatura: {data['temperature']} °C")
                self.humidity_label.setText(f"Umidade: {data['humidity']} %")
                self.gas_label.setText(f"Gás: {data['gas']}")
            else:
                self.temperature_label.setText("Erro ao obter dados.")
                self.humidity_label.setText("Erro ao obter dados.")
                self.gas_label.setText("Erro ao obter dados.")
        except requests.exceptions.RequestException as e:
            print(f"Erro: {e}")
            self.temperature_label.setText("Erro de conexão!")
            self.humidity_label.setText("Erro de conexão!")
            self.gas_label.setText("Erro de conexão!")

app = QApplication(sys.argv)
window = SensorApp()
window.show()
sys.exit(app.exec())
