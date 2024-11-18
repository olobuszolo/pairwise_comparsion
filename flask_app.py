from flask import Flask, request, jsonify, render_template, send_file
import numpy as np
import json
from AHPModel import AHPModel
import io

app = Flask(__name__)

ahp = AHPModel()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_alternative', methods=['POST'])
def add_alternative():
    data = request.json
    alternative_name = data.get('alternative_name')
    if alternative_name:
        ahp.add_alternative(alternative_name)
        return jsonify({'message': 'Alternative added successfully'}), 200
    return jsonify({'error': 'No alternative name provided'}), 400

@app.route('/add_criterion', methods=['POST'])
def add_criterion():
    data = request.json
    criterion_name = data.get('criterion_name')
    if criterion_name:
        ahp.add_criterion(criterion_name)
        return jsonify({'message': 'Criterion added successfully'}), 200
    return jsonify({'error': 'No criterion name provided'}), 400

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

@app.route('/calculate_final_ranking', methods=['GET'])
def calculate_final_ranking():
    try:
        ranking = ahp.calculate_final_ranking()
        ranking_list = [{'alternative': alternative, 'score': score} for alternative, score in ranking]
        return jsonify({'ranking': ranking_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/download_model', methods=['GET'])
def download_model():
    try:
        filename = request.args.get('filename', 'ahp_model.json')
        data = {
            'alternatives': ahp.alternatives,
            'criteria': ahp.criteria,
            'expert_matrices': {
                expert: {
                    criterion: matrix.tolist()
                    for criterion, matrix in matrices.items()
                }
                for expert, matrices in ahp.expert_matrices.items()
            }
        }
        file_stream = io.StringIO()
        json.dump(data, file_stream, indent=4)
        file_stream.seek(0)

        return send_file(
            io.BytesIO(file_stream.getvalue().encode()),
            mimetype='application/json',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/upload_model', methods=['POST'])
def upload_model():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.json'):
        try:
            content = json.load(file)
            ahp.load_from_file(content)
            return jsonify({'message': 'Model parameters uploaded successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    return jsonify({'error': 'Invalid file type, only JSON allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True)
