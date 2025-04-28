from flask import Flask, render_template, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index/index.html')

@app.route('/sobre')
def sobre():
    return render_template('index/sobre.html', titulo='Sobre Nós')

@app.route('/api/heatmap')
def heatmap_data():
    # Dados mockados para teste
    return jsonify([
        {'setor': 'UTI', 'ocupacao': 15, 'capacidade': 20, 'taxa_ocupacao': 75.0},
        {'setor': 'Emergencia', 'ocupacao': 25, 'capacidade': 30, 'taxa_ocupacao': 83.3},
        {'setor': 'Pediatria', 'ocupacao': 18, 'capacidade': 25, 'taxa_ocupacao': 72.0},
        {'setor': 'Cardiologia', 'ocupacao': 12, 'capacidade': 15, 'taxa_ocupacao': 80.0},
        {'setor': 'Ortopedia', 'ocupacao': 16, 'capacidade': 20, 'taxa_ocupacao': 80.0}
    ])

@app.route('/api/dashboard/stats')
def dashboard_stats():
    # Dados mockados para teste
    return jsonify({
        'total_internados': 86,
        'atendimentos_hoje': 42,
        'tempo_medio_atendimento': 45.5
    })

@app.route('/api/dashboard/ocupacao')
def dashboard_ocupacao():
    # Dados mockados para teste
    return jsonify([
        {'dia': '19/04', 'ocupacao': 75},
        {'dia': '20/04', 'ocupacao': 82},
        {'dia': '21/04', 'ocupacao': 78},
        {'dia': '22/04', 'ocupacao': 85},
        {'dia': '23/04', 'ocupacao': 90},
        {'dia': '24/04', 'ocupacao': 86},
        {'dia': '25/04', 'ocupacao': 88}
    ])

if __name__ == '__main__':
    app.run(debug=True, port=3000)
