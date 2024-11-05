from flask import Flask, request, jsonify, render_template
import numpy as np
import json
from AHPModel import AHPModel  # Importujemy model AHP

app = Flask(__name__)

# Inicjalizacja modelu AHP
ahp = AHPModel()

# Strona główna aplikacji
@app.route('/')
def index():
    return render_template('index.html')

# Dodawanie alternatywy
@app.route('/add_alternative', methods=['POST'])
def add_alternative():
    data = request.json
    alternative_name = data.get('alternative_name')
    if alternative_name:
        ahp.add_alternative(alternative_name)
        return jsonify({'message': 'Alternative added successfully'}), 200
    return jsonify({'error': 'No alternative name provided'}), 400

# Dodawanie kryterium
@app.route('/add_criterion', methods=['POST'])
def add_criterion():
    data = request.json
    criterion_name = data.get('criterion_name')
    if criterion_name:
        ahp.add_criterion(criterion_name)
        return jsonify({'message': 'Criterion added successfully'}), 200
    return jsonify({'error': 'No criterion name provided'}), 400

# Dodawanie macierzy porównań eksperta
@app.route('/add_expert_matrix', methods=['POST'])
def add_expert_matrix():
    data = request.json
    expert_name = data.get('expert_name')
    criterion = data.get('criterion')
    matrix = data.get('matrix')
    if expert_name and criterion and matrix:
        try:
            matrix_np = np.array(matrix)
            ahp.add_expert_matrix(expert_name, criterion, matrix_np)
            return jsonify({'message': 'Expert matrix added successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    return jsonify({'error': 'Missing data for expert name, criterion or matrix'}), 400

# Obliczanie rankingu końcowego
@app.route('/calculate_final_ranking', methods=['GET'])
def calculate_final_ranking():
    try:
        ranking = ahp.calculate_final_ranking()
        ranking_list = [{'alternative': alternative, 'score': score} for alternative, score in ranking]
        return jsonify({'ranking': ranking_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Zapis do pliku
@app.route('/save', methods=['POST'])
def save_to_file():
    data = request.json
    filename = data.get('filename', 'ahp_model.json')
    try:
        ahp.save_to_file(filename)
        return jsonify({'message': 'Model saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Odczyt z pliku
@app.route('/load', methods=['POST'])
def load_from_file():
    data = request.json
    filename = data.get('filename', 'ahp_model.json')
    try:
        ahp.load_from_file(filename)
        return jsonify({'message': 'Model loaded successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
