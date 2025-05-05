from aa.db.connection import get_connection


def fetch_all_cliente():
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cliente")
        clientes = cursor.fetchall()
        return clientes
    except Exception as e:
        print(f"Erro ao buscar clientes: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def salvar_cliente_db(nome, endereco):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO cliente (nome, endereco) VALUES (%s, %s)", (nome, endereco))
            conn.commit()
        except Exception as e:
            print(f"Erro ao salvar cliente: {e}")
        finally:
            cursor.close()
            conn.close()
