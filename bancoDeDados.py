import sqlite3
import pandas as pd
from datetime import datetime

class SelecaoBD:

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.open_connection()

    def open_connection(self):
        if not self.connection:
            self.connection = sqlite3.connect("dados_gas_alcool_etanol.db")
            self.cursor = self.connection.cursor()

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None

    def media_por_minuto(self):
        
        self.cursor.execute('''
            SELECT 
                strftime('%Y-%m-%d %H:%M', datetime('now')) AS minuto,
                AVG(temperatura) AS media_temperatura,
                AVG(umidade) AS media_umidade,
                AVG(concentracao) AS media_concentracao
            FROM dados_gas_temp_umi
            GROUP BY minuto
        ''')
        resultados = self.cursor.fetchall()

        string_resultados = "Média por Minuto:\n"
        for linha in resultados:
            minuto, media_temp, media_umi, media_conc = linha
            string_resultados += (f"Minuto: {minuto} | "
                                  f"Temperatura Média: {media_temp:.2f} | "
                                  f"Umidade Média: {media_umi:.2f} | "
                                  f"Concentração Média: {media_conc:.2f}\n")
        print(string_resultados)
        return string_resultados
    
    def __del__(self):
        self.close_connection()

class RegistroBD:

    def __init__(self, concentracao, temp, umi):
        self.concentracao = concentracao
        self.temp = temp
        self.umidade = umi
        self.connection = None
        self.cursor = None
        self.open_connection()

    def open_connection(self):
        if not self.connection:
            self.connection = sqlite3.connect("dados_gas_alcool_etanol.db")
            self.cursor = self.connection.cursor()

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
    
    def registro_leitura(self):
        
        #data_hora = datetime.now().isoformat()
    
        # Inserir os dados no banco de dados
        self.cursor.execute('''
            INSERT INTO dados_gas_temp_umi (
                temperatura,
                umidade,
                concentracao
            ) VALUES (?, ?, ?)
        ''', [self.temp, self.umidade, self.concentracao])
    
        self.connection.commit()
        print(f"Dados registrados com sucesso.")

    def __del__(self):
        self.close_connection()

if __name__ == '__main__':
    pass