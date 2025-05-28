from flask import Flask, render_template, request, redirect
from aa.controllers.cliente_controller import fetch_all_cliente, salvar_cliente_db
from aa.controllers.produto_controller import fetch_all_produto, salvar_produto_db
from aa.db.connection import get_connection

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/gerenciamento')
def gerenciamento():
    return render_template('gerenciamento.html')

@app.route('/cadastro_cliente')
def cadastro_cliente():
    return render_template('cadastro_cliente.html')

@app.route('/cadastro_produto')
def cadastro_produto():
    return render_template('cadastro_produto.html')

@app.route('/salvar_cliente', methods=['POST'])
def salvar_cliente():
    nome = request.form.get('nome')
    endereco = request.form.get('endereco')
    salvar_cliente_db(nome, endereco)
    return redirect('/gerenciamento')

@app.route('/salvar_produto', methods=['POST'])
def salvar_produto():
    codproduto = request.form['codproduto']
    nome = request.form['nome']
    preco = request.form['preco']

    mensagem = salvar_produto_db(codproduto, nome, preco)

    return render_template('cadastro_produto.html', mensagem=mensagem)


@app.route('/listar_clientes')
def listar_clientes():
    clientes = fetch_all_cliente()
    return render_template('lista_clientes.html', clientes=clientes)

@app.route('/listar_produtos')
def listar_produtos():
    produtos = fetch_all_produto()
    return render_template('lista_produtos.html', produtos=produtos)

@app.route('/deletar_produto/<int:idproduto>')
def deletar_produto(idproduto):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM produto WHERE idproduto = %s", (idproduto,))
            conn.commit()
        except Exception as e:
            print(f"Erro ao excluir produto: {e}")
        finally:
            cursor.close()
            conn.close()

    return redirect('/listar_produtos')

@app.route('/editar_produto/<int:idproduto>', methods=['GET'])
def editar_produto(idproduto):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM produto WHERE idproduto = %s", (idproduto,))
            produto = cursor.fetchone()

            if not produto:
                return "❌ Produto não encontrado!", 404  # Retorna erro se o produto não existir

            return render_template('editar_produto.html', produto=produto)
        except Exception as e:
            return f"Erro ao buscar produto: {e}", 500
        finally:
            cursor.close()
            conn.close()

@app.route('/atualizar_produto/<int:idproduto>', methods=['POST'])
def atualizar_produto(idproduto):
    nome = request.form['nome']
    preco = request.form['preco']

    try:
        preco = float(preco)
        if preco <= 0:
            return "❌ O preço deve ser maior que zero!", 400
    except ValueError:
        return "❌ O preço precisa ser um valor numérico válido!", 400

    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE produto SET nome = %s, preco = %s WHERE idproduto = %s", (nome, preco, idproduto))
            conn.commit()
            return redirect('/listar_produtos')
        except Exception as e:
            return f"Erro ao atualizar produto: {e}", 500
        finally:
            cursor.close()
            conn.close()


@app.route('/registrar_venda', methods=['POST'])
def registrar_venda():
    codcliente = request.form.get('codcliente')
    produtos_selecionados = request.form.get("produtos_selecionados")

    if not codcliente or not produtos_selecionados:
        return "❌ Erro: Cliente e produtos precisam ser selecionados!", 400

    produtos_selecionados = produtos_selecionados.split(",")

    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()

            # 🔹 Criar a venda na tabela `Venda`
            cursor.execute("INSERT INTO venda (codcliente, data, valortotal) VALUES (%s, NOW(), 0)", (codcliente,))
            conn.commit()
            codvenda = cursor.lastrowid

            valor_total = 0

            # 🔹 Registrar cada item vendido e calcular corretamente o valor total
            for item in produtos_selecionados:
                codproduto, quantidade = item.split(":")
                quantidade = int(quantidade)

                cursor.execute("SELECT preco FROM produto WHERE idproduto = %s", (codproduto,))
                preco = cursor.fetchone()[0]
                valor_item = float(preco) * quantidade
                valor_total += valor_item

                cursor.execute("INSERT INTO item_venda (codvenda, codproduto, quantidade, valor) VALUES (%s, %s, %s, %s)",
                               (codvenda, codproduto, quantidade, valor_item))
                conn.commit()

            # 🔹 Atualizar `valortotal` da venda com o valor somado corretamente
            cursor.execute("UPDATE venda SET valortotal = %s WHERE idvenda = %s", (valor_total, codvenda))
            conn.commit()

            return render_template("confirmacao_venda.html", codvenda=codvenda, valor_total=valor_total)
        except Exception as e:
            return f"Erro ao registrar venda: {e}", 500
        finally:
            cursor.close()
            conn.close()


@app.route('/buscar_vendas', methods=['GET'])
def buscar_vendas():
    codigo_venda = request.args.get('codigo_venda')

    conn = get_connection()
    vendas = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT v.idvenda, c.nome AS cliente, p.nome AS produto, iv.quantidade, v.data
                FROM venda v
                JOIN cliente c ON v.codcliente = c.idcliente
                JOIN item_venda iv ON v.idvenda = iv.codvenda  -- 🔥 Pegando os itens da venda corretamente
                JOIN produto p ON iv.codproduto = p.idproduto
                WHERE v.idvenda = %s
            """, (codigo_venda,))
            vendas = cursor.fetchall()
        except Exception as e:
            return f"Erro ao buscar venda: {e}", 500
        finally:
            cursor.close()
            conn.close()

    return render_template('listar_vendas.html', vendas=vendas)


@app.route('/efetuar_venda', methods=['GET'])
def efetuar_venda():
    conn = get_connection()
    clientes = []
    produtos = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT idcliente, nome FROM cliente")
            clientes = cursor.fetchall()

            cursor.execute("SELECT idproduto, nome, preco FROM produto")
            produtos = cursor.fetchall()

        except Exception as e:
            print(f"Erro ao buscar clientes/produtos: {e}")
        finally:
            cursor.close()
            conn.close()

    return render_template('efetuar_venda.html', clientes=clientes, produtos=produtos)


@app.route('/listar_vendas', methods=['GET'])
def listar_vendas():
    conn = get_connection()
    vendas = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM venda")
            vendas = cursor.fetchall()
        except Exception as e:
            return f"Erro ao listar vendas: {e}", 500
        finally:
            cursor.close()
            conn.close()

    return render_template("listar_vendas.html", vendas=vendas)

@app.route('/excluir_cliente/<int:idcliente>')
def excluir_cliente(idcliente):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cliente WHERE idcliente = %s", (idcliente,))
            conn.commit()
        except Exception as e:
            print(f"Erro ao excluir cliente: {e}")
        finally:
            cursor.close()
            conn.close()

    return redirect('/listar_clientes')

@app.route('/editar_cliente/<int:idcliente>', methods=['GET'])
def editar_cliente(idcliente):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cliente WHERE idcliente = %s", (idcliente,))
            cliente = cursor.fetchone()

            if not cliente:
                return "❌ Cliente não encontrado!", 404

            return render_template('editar_cliente.html', cliente=cliente)
        except Exception as e:
            return f"Erro ao buscar cliente: {e}", 500
        finally:
            cursor.close()
            conn.close()

@app.route('/atualizar_cliente/<int:idcliente>', methods=['POST'])
def atualizar_cliente(idcliente):
    nome = request.form['nome']
    endereco = request.form['endereco']

    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE cliente SET nome = %s, endereco = %s WHERE idcliente = %s", (nome, endereco, idcliente))
            conn.commit()
            return redirect('/listar_clientes')
        except Exception as e:
            return f"Erro ao atualizar cliente: {e}", 500
        finally:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

