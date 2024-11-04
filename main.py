import re
import sqlite3

# Caminho para o arquivo de log
log_file_path = r'LOGS_FILE_PATH.txt'

# Conexão ao banco de dados SQLite
conn = sqlite3.connect('logs.db')
cursor = conn.cursor()

# Criação da tabela (se ainda não existir)
cursor.execute('''
CREATE TABLE IF NOT EXISTS log_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    log_level TEXT,
    thread_id INTEGER,
    exception TEXT
)
''')

# Expressão regular para extrair as informações desejadas da linha de log
log_pattern = re.compile(
    r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})\s+'
    r'(?P<log_level>\w+)\s+'
    r'(?P<thread_id>\d+)\s+---\s+\[.*?\]\s+.*?\s+:\s+.*?'
    r'(?P<exception>[a-zA-Z0-9_.]+Exception: .*?)$'
)

# Leitura e processamento do arquivo de log
with open(log_file_path, 'r') as file:
    for line in file:
        match = log_pattern.search(line)
        if match:
            log_data = match.groupdict()

            # Inserção dos dados na tabela
            cursor.execute('''
            INSERT INTO log_entries (timestamp, log_level, thread_id, exception)
            VALUES (?, ?, ?, ?)
            ''', (
                log_data['timestamp'], 
                log_data['log_level'], 
                int(log_data['thread_id']), 
                log_data['exception']
            ))

# Commit e fechamento da conexão
conn.commit()
cursor.close()
conn.close()
