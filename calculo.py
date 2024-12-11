import sqlite3

class MediaDados:
    def __init__(self):
        self.db_path = "dados_gas_alcool_etanol.db"
        self.table_name = "dados_gas_alcool_etanol"
        self.results = None

    def calculo_media(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            query = f"""
            SELECT 
                strftime('%Y-%m-%d %H:%M', datetime_column) AS minute,
                AVG(temperature) AS avg_temperature,
                AVG(humidity) AS avg_humidity,
                AVG(gas_concentration) AS avg_gas_concentration
            FROM 
                {self.table_name}
            GROUP BY 
                strftime('%Y-%m-%d %H:%M', datetime_column);
            """
            
            print("concluido")    
            cursor.execute(query)
            self.results = cursor.fetchall()
            #return self.results
        
        except sqlite3.Error as e:
            print(f"Erro ao acessar o banco de dados: {e}")
            return []
        finally:
            conn.close()

    def display_results(self):
        """
        Exibe os resultados no console.

        :param results: Lista de resultados retornados pela consulta SQL.
        """
        self.calculate_averages_per_minute
        print("Média por minuto:")
        for row in self.results:
            print(f"Minuto: {row[0]}, Temperatura média: {row[1]:.2f}, "
                  f"Umidade média: {row[2]:.2f}, Gás média: {row[3]:.2f}")
            return (f"Minuto: {row[0]}, Temperatura média: {row[1]:.2f}, "
                  f"Umidade média: {row[2]:.2f}, Gás média: {row[3]:.2f}")

# Exemplo de uso
if __name__ == "__main__":
    # Inicializa a classe com o caminho para o banco de dados e o nome da tabela
    aggregator = DataAggregator
    
    # Calcula as médias por minuto
    aggregator.calculate_averages_per_minute
    
    # Exibe os resultados
    aggregator.display_results
