from flask import Flask, jsonify, request
import psycopg2
import pymysql

app = Flask(__name__)

pg_connection = {
    'host': 'postgres',
    'port': 5432, 
    'database': 'mydb',
    'user': 'myuser',
    'password': 'mypassword',
}

mysql_connection = {
    'host': 'mysql',
    'port': 3306, 
    'database': 'mydb',
    'user': 'myuser',
    'password': 'mypassword',
}

@app.route('/')
def test():
    return 'test'

@app.route('/comidas', methods=['GET'])
def listar_comidas():
    conn = psycopg2.connect(**pg_connection)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comidas')
    comidas = cursor.fetchall()
    conn.close()
    return jsonify(comidas)

@app.route('/adicionar_comida', methods=['POST'])
def adicionar_comida_pg():
    try:
        conn = psycopg2.connect(**pg_connection)
        cursor = conn.cursor()

        nome_comida = request.json['nome_comida']

        cursor.execute("INSERT INTO comidas (nome) VALUES (%s)", (nome_comida,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Comida adicionada com sucesso."})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/filmes', methods=['GET'])
def listar_filmes():
    conn = pymysql.connect(**mysql_connection)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM filmes')
    filmes = cursor.fetchall()
    conn.close()
    return jsonify(filmes)

@app.route('/adicionar_filme', methods=['POST'])
def adicionar_filme_mysql():
    try:
        conn = pymysql.connect(**mysql_connection)
        cursor = conn.cursor()

        nome_filme = request.json['nome_filme']

        cursor.execute("INSERT INTO filmes (titulo) VALUES (%s)", (nome_filme,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Filme adicionado com sucesso."})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/verificar_item', methods=['POST'])
def verificar_item():
    item = request.json['item']

    conn_pg = psycopg2.connect(**pg_connection)
    cursor_pg = conn_pg.cursor()
    cursor_pg.execute("SELECT nome FROM comidas WHERE nome = %s", (item,))
    result_pg = cursor_pg.fetchone()
    conn_pg.close()

    conn_mysql = pymysql.connect(**mysql_connection)
    cursor_mysql = conn_mysql.cursor()
    cursor_mysql.execute("SELECT titulo FROM filmes WHERE titulo = %s", (item,))
    result_mysql = cursor_mysql.fetchone()
    conn_mysql.close()

    return jsonify({"presente_em_comidas": bool(result_pg), "presente_em_filmes": bool(result_mysql)})



if __name__ == '__main__':
    app.run(debug=True)
