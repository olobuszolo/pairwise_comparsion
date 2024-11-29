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
        filled_matrix = self.fill_missing_values(np.array(matrix))
        self.expert_matrices[expert_name][criterion] = filled_matrix


    def calculate_inconsistency_index(self, matrix):
        eigval, _ = np.linalg.eig(matrix)
        max_eigval = max(eigval.real)
        n = matrix.shape[0]
        ci = (max_eigval - n) / (n - 1)
        return ci
    
    def calculate_final_ranking_topsis(self):
        aggregated_matrices = {}
        for criterion in self.criteria:
            matrices = [self.expert_matrices[expert][criterion] for expert in self.expert_matrices if criterion in self.expert_matrices[expert]]
            aggregated_matrices[criterion] = sum(matrices) / len(matrices)

        criterion_weights = []
        local_priorities = []
        for criterion in self.criteria:
            matrix = aggregated_matrices[criterion]
            norm_matrix = matrix / matrix.sum(axis=0)  
            weights = norm_matrix.mean(axis=1)
            criterion_weights.append(weights)
            local_priorities.append(weights)

        local_priorities = np.array(local_priorities).T
        weights = np.ones(len(self.criteria)) / len(self.criteria) 

        normalized_matrix = local_priorities / np.sqrt((local_priorities**2).sum(axis=0))

        weighted_matrix = normalized_matrix * weights

        ideal_solution = weighted_matrix.max(axis=0) 
        anti_ideal_solution = weighted_matrix.min(axis=0)

        distance_to_ideal = np.sqrt(((weighted_matrix - ideal_solution)**2).sum(axis=1))
        distance_to_anti_ideal = np.sqrt(((weighted_matrix - anti_ideal_solution)**2).sum(axis=1))

        closeness_coefficient = distance_to_anti_ideal / (distance_to_ideal + distance_to_anti_ideal)

        final_ranking = sorted([(self.alternatives[i], closeness) for i, closeness in enumerate(closeness_coefficient)], key=lambda x: x[1], reverse=True)

        return final_ranking
    

    def calculate_final_ranking_consistency_adjusted(self):
        aggregated_matrices = {}
        consistency_weights = {}

        for criterion in self.criteria:
            matrices = [self.expert_matrices[expert][criterion] for expert in self.expert_matrices if criterion in self.expert_matrices[expert]]
            consistencies = [self.calculate_inconsistency_index(matrix) for matrix in matrices]

            max_consistency = max(consistencies) if consistencies else 1  
            weights = [(max_consistency - ci) / max_consistency if max_consistency > 0 and ci < max_consistency else 0 for ci in consistencies]

            if sum(weights) > 0:
                weights = np.array(weights) / sum(weights)
            else:
                weights = np.ones(len(weights)) / len(weights) 

            aggregated_matrices[criterion] = sum(w * m for w, m in zip(weights, matrices)) if matrices else np.ones((len(self.alternatives), len(self.alternatives)))
            consistency_weights[criterion] = weights

        criterion_weights = []
        for criterion in self.criteria:
            matrix = aggregated_matrices[criterion]
            norm_matrix = matrix / matrix.sum(axis=0) if matrix.sum(axis=0).all() else matrix 
            weights = norm_matrix.mean(axis=1)
            criterion_weights.append(weights)

        final_scores = np.zeros(len(self.alternatives))
        for i, weights in enumerate(criterion_weights):
            final_scores += weights
        final_ranking = final_scores / len(self.criteria)

        return sorted([(self.alternatives[i], score) for i, score in enumerate(final_ranking)], key=lambda x: x[1], reverse=True)


    def calculate_final_ranking_basic(self):
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

        return sorted([(self.alternatives[i], score) for i, score in enumerate(final_ranking)], key=lambda x: x[1], reverse=True)

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
    
    def clear_model(self):
        self.alternatives = []
        self.criteria = []
        self.expert_matrices = {}
        
    def get_inconsistency_indices(self):
        inconsistency_indices = {}
        for expert in self.expert_matrices:
            inconsistency_indices[expert] = {}
            for criterion in self.expert_matrices[expert]:
                matrix = self.expert_matrices[expert][criterion]
                inconsistency_indices[expert][criterion] = self.calculate_inconsistency_index(np.array(matrix))
        return inconsistency_indices
    
    def get_criteria(self):
        return self.criteria
    
    def get_number_of_alternatives(self):
        return len(self.alternatives)
    
    def fill_missing_values(self, matrix):
        n = matrix.shape[0]
        filled_matrix = matrix.copy()

        for i in range(n):
            for j in range(n):
                if np.isnan(filled_matrix[i, j]): 
                    for k in range(n):
                        if not np.isnan(filled_matrix[i, k]) and not np.isnan(filled_matrix[k, j]):
                            filled_matrix[i, j] = filled_matrix[i, k] * filled_matrix[k, j]
                            break
                    if np.isnan(filled_matrix[i, j]):
                        filled_matrix[i, j] = 1.0
        np.fill_diagonal(filled_matrix, 1.0)
        return filled_matrix
