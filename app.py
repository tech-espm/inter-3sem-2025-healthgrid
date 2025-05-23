from flask import Flask, render_template, json, jsonify, request, Response
import config
import requests
import banco
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index/index.html')

@app.route('/sobre')
def sobre():
    return render_template('index/sobre.html', titulo='Sobre Nós')

@app.route('/api/ocupacao')
def ocupacao():
    # Obter o maior id do banco
    maior_id = banco.obterIdMaximo("pca")
    if maior_id < 800000:
        maior_id = 800000

    resultado = requests.get(f'{config.url_api}?sensor=pca&id_inferior={maior_id}')
    dados_novos = resultado.json()

    # Inserir os dados novos no banco
    if dados_novos and len(dados_novos) > 0:
        banco.inserirDados(dados_novos)

    dados = banco.listarTempoReal()

    consolidados = [
        { 'id_especialidade': 1, 'especialidade': 'Pediatria', 'ocupacao': 0, 'capacidade': 0, 'taxa_ocupacao': 0 },
        { 'id_especialidade': 2, 'especialidade': 'UTI', 'ocupacao': 0, 'capacidade': 0, 'taxa_ocupacao': 0 },
    ]

    for dado in dados:
        consolidado = consolidados[dado['id_especialidade'] - 1]
        dado['especialidade'] = consolidado['especialidade']
        if dado['ocupacao'] == 1:
            consolidado['ocupacao'] += 1
        consolidado['capacidade'] += 1

    for consolidado in consolidados:
        if consolidado['capacidade'] > 0:
            consolidado['taxa_ocupacao'] = 100 * consolidado['ocupacao'] / consolidado['capacidade']

    return jsonify({
        'dados': dados,
        'consolidados': consolidados
	})

@app.get('/api/historico')
def historico():
    # Obter o maior id do banco
    maior_id = banco.obterIdMaximo("pca")
    if maior_id < 800000:
        maior_id = 800000

    resultado = requests.get(f'{config.url_api}?sensor=pca&id_inferior={maior_id}')
    dados_novos = resultado.json()

    # Inserir os dados novos no banco
    if dados_novos and len(dados_novos) > 0:
        banco.inserirDados(dados_novos)

    dataInicial = request.args["dataInicial"]
    dataFinal = request.args["dataFinal"]
    dados = banco.listarHistorico(dataInicial, dataFinal)

    return json.jsonify(dados)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
