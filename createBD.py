import sqlite3

conexao = sqlite3.connect("dados_gas_alcool_etanol.db")
cursor = conexao.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS dados_gas_temp_umi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperatura FLOAT,
    umidade INT,
    concentracao INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
conexao.commit()