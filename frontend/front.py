from flask import Flask, render_template, request, url_for, redirect
import requests

app = Flask(__name__)

backend_url = "http://backend:5000"

@app.route('/')
def index_root():
    return "Digite na url: /filmes, /comidas ou /verificar_item"

@app.route('/filmes')
def index_filmes():
    response_filmes = requests.get(f"{backend_url}/filmes")
    
    if response_filmes.status_code == 200:
        filmes = response_filmes.json()
    else:
        filmes = []

    return render_template('filmes.html', filmes=filmes)

@app.route('/comidas')
def index_comidas():
    response_comidas = requests.get(f"{backend_url}/comidas")
    
    if response_comidas.status_code == 200:
        comidas = response_comidas.json()
    else:
        comidas = []

    return render_template('comidas.html', comidas=comidas)

@app.route('/adicionar_comida', methods=['POST'])
def adicionar_comida_frontend():
    nome_comida = request.form['nome_comida']

    response = requests.post(f"{backend_url}/adicionar_comida", json={'nome_comida': nome_comida})

    if response.status_code == 200:
        return redirect(url_for('index_comidas'))
    else:
        return "Erro ao adicionar comida."
    
@app.route('/adicionar_filme', methods=['POST'])
def adicionar_filme_frontend():
    nome_filme = request.form['nome_filme']

    response = requests.post(f"{backend_url}/adicionar_filme", json={'nome_filme': nome_filme})

    if response.status_code == 200:
        return redirect(url_for('index_filmes'))
    else:
        return "Erro ao adicionar filme."

@app.route('/verificar_item', methods=['GET'])
def index_verificar_item():
    return render_template('verificar_item.html')

@app.route('/verificar_item', methods=['POST'])
def verificar_item_frontend():
    item = request.form['item']

    response = requests.post(f"{backend_url}/verificar_item", json={'item': item})

    if response.status_code == 200:
        resultado = response.json()
        presente_em_comidas = resultado['presente_em_comidas']
        presente_em_filmes = resultado['presente_em_filmes']
        return render_template('verificar_item_resultado.html', item=item, presente_em_comidas=presente_em_comidas, presente_em_filmes=presente_em_filmes)
    else:
        return "Erro ao verificar o item."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
