import re
import sqlite3

log_file_path = r'ADICIONE O CAMINHO PARA ARQUIVO DE LOG .txt'

conn = sqlite3.connect('logs.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE log_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    log_level TEXT,
    thread_id INTEGER,
    is_exception BOOLEAN,
    exception TEXT,
    message TEXT
)
''')

# Expressão regular para identificar a exceção
exception_pattern = re.compile(r'(?P<exception>[a-zA-Z0-9_.]+Exception):')

# Expressão regular do cabeçalho
header_pattern = re.compile(
    r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})\s+'
    r'(?P<log_level>\w+)\s+'
    r'(?P<thread_id>\d+)'
)

# Leitura e processamento do arquivo de log
with open(log_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        print(f"Processando linha: {line.strip()}")  # Debugging print

        parts = line.split(' --- ', 1)
        if len(parts) < 2:
            print(f"Formato inesperado para a linha: {line.strip()}")
            continue
        
        header_part = parts[0].strip()
        message_part = parts[1].strip()

        header_match = header_pattern.match(header_part)
        if not header_match:
            print(f"Erro ao analisar header da linha: {line.strip()}")
            continue
        
        header_data = header_match.groupdict()

        exception_match = exception_pattern.search(message_part)
        if exception_match:
            exception_name = exception_match.group('exception')
            is_exception = True
        else:
            exception_name = None
            is_exception = False

        message_start = message_part.find(']')
        message_text = message_part[message_start + 1:].strip() if message_start != -1 else message_part

        # Inserção dos dados na tabela log_entries
        cursor.execute('''
        INSERT INTO log_entries (timestamp, log_level, thread_id, is_exception, exception, message)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            header_data['timestamp'],
            header_data['log_level'],
            int(header_data['thread_id']),
            is_exception,
            exception_name,
            message_text
        ))

conn.commit()
cursor.close()
conn.close()