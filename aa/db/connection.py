import mysql.connector

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="177.190.74.69",        # Endereço do servidor
            user="trabtpc",              # Substitua pelo usuário do MySQL
            password="trabtpc",          # Substitua pela sua senha
            database="tpc13",            # Nome do banco no Workbench
            port=65004,                   # Certifique-se de que essa porta está aberta
        )
        if conn.is_connected():
            print("✅ Conexão bem-sucedida ao MySQL via DataGrip!")
        return conn
    except mysql.connector.Error as e:
        print(f"❌ Erro ao conectar ao MySQL: {e}")
        return None

# Teste a conexão
connection = get_connection()
if connection:
    connection.close()
