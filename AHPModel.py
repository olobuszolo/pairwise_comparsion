import numpy as np
import json

class AHPModel:
    def __init__(self):
        self.alternatives = []
        self.criteria = []
        self.expert_matrices = {}

    def add_alternative(self, alternative_name):
        self.alternatives.append(alternative_name)

    def add_criterion(self, criterion_name):
        self.criteria.append(criterion_name)

    def add_expert_matrix(self, expert_name, criterion, matrix):
        if criterion not in self.criteria:
            print(f"Criterion '{criterion}' not found.")
            return
        if expert_name not in self.expert_matrices:
            self.expert_matrices[expert_name] = {}
        self.expert_matrices[expert_name][criterion] = matrix

    def calculate_inconsistency_index(self, matrix):
        eigval, _ = np.linalg.eig(matrix)
        max_eigval = max(eigval)
        n = matrix.shape[0]
        ci = (max_eigval - n) / (n - 1)
        return ci

    def calculate_final_ranking(self):
        aggregated_matrices = {}
        for criterion in self.criteria:
            matrices = [self.expert_matrices[expert][criterion] for expert in self.expert_matrices if criterion in self.expert_matrices[expert]]
            aggregated_matrices[criterion] = sum(matrices) / len(matrices)

        criterion_weights = []
        for criterion in self.criteria:
            matrix = aggregated_matrices[criterion]
            norm_matrix = matrix / matrix.sum(axis=0)
            weights = norm_matrix.mean(axis=1)
            criterion_weights.append(weights)

        final_scores = np.zeros(len(self.alternatives))
        for i, weights in enumerate(criterion_weights):
            final_scores += weights
        final_ranking = final_scores / len(self.criteria)

        return [(self.alternatives[i], score) for i, score in enumerate(final_ranking)]

    def save_to_file(self, filename):
        data = {
            'alternatives': self.alternatives,
            'criteria': self.criteria,
            'expert_matrices': self.expert_matrices
        }
        data = self._convert_ndarrays_to_lists(data)
        
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def _convert_ndarrays_to_lists(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: self._convert_ndarrays_to_lists(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_ndarrays_to_lists(item) for item in obj]
        else:
            return obj
        
    def load_from_file(self, data):
        self.alternatives = data['alternatives']
        self.criteria = data['criteria']
        self.expert_matrices = data.get("expert_matrices", {})
        for expert in self.expert_matrices:
            for criterion in self.expert_matrices[expert]:
                self.expert_matrices[expert][criterion] = np.array(self.expert_matrices[expert][criterion])