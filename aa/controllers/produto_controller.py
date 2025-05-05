from aa.db.connection import get_connection

def fetch_all_produto():
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produto")
        produtos = cursor.fetchall()
        return produtos
    except Exception as e:
        print(f"Erro ao buscar produtos: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def salvar_produto_db(codproduto, nome, preco):
    try:
        preco = float(preco)
        if preco <= 0:
            return "❌ O preço deve ser maior que zero!"

    except ValueError:
        return "❌ O preço precisa ser um valor numérico válido!"

    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()

            # Verifica se o código já existe
            cursor.execute("SELECT COUNT(*) FROM produto WHERE idproduto = %s", (codproduto,))
            existe = cursor.fetchone()[0]

            if existe > 0:
                return "❌ Código já existente! Por favor, digite um novo código."

            # Insere o produto no banco
            cursor.execute("INSERT INTO produto (idproduto, nome, preco) VALUES (%s, %s, %s)",
                           (codproduto, nome, preco))
            conn.commit()
            return "✅ Produto cadastrado com sucesso!"
        except Exception as e:
            return f"Erro ao cadastrar produto: {e}"
        finally:
            cursor.close()
            conn.close()

