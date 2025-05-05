from aa.db.connection import get_connection
from aa.models.venda import Venda

def fetch_all_venda():
    conn = get_connection()
    if not conn:
        print("Conexão não está disponível.")
        return []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produto")
    venda_data = cursor.fetchall()
    conn.close()

    vendas = [
        Venda(
            idvenda=row[0],
            data=row[1],
            valortotal=row[2],
            codcliente=row[3]
        )
        for row in venda_data
    ]
    return vendas