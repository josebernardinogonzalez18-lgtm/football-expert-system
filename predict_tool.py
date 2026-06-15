import sys
import json
import numpy as np
from scipy.stats import poisson
import os

class ExpertFootballSystem:
    def __init__(self):
        self.version = "5.0-Param-Optimized"
        # Cargar parámetros mejorados si existen
        if os.path.exists('model_params.json'):
            with open('model_params.json', 'r') as f:
                self.params = json.load(f)
        else:
            self.params = {"k_factor": 32, "dynamic_xg_bias": 0.10}

    def calculate_poisson(self, h_xg, a_xg):
        # Aplicar sesgo dinámico basado en aprendizaje previo
        bias = self.params.get("dynamic_xg_bias", 0.10)
        h_xg_adj = h_xg * (1 + bias)
        a_xg_adj = a_xg * (1 - bias / 2)
        
        h_probs = poisson.pmf(range(7), h_xg_adj)
        a_probs = poisson.pmf(range(7), a_xg_adj)
        m = np.outer(h_probs, a_probs)
        return float(np.sum(np.tril(m, -1))), float(np.sum(np.diag(m))), float(np.sum(np.triu(m, 1)))

    def run_inference(self, match_data):
        p1, px, p2 = self.calculate_poisson(match_data['h_xg'], match_data['a_xg'])
        best_prob = max(p1, px, p2)
        label = {p1: '1', px: 'X', p2: '2'}[best_prob]
        odds = match_data['odds'][label]
        
        # Kelly fraccional dinámico según K-Factor
        fraction = 0.25 if self.params['k_factor'] < 35 else 0.15
        kelly = (best_prob * (odds - 1) - (1 - best_prob)) / (odds - 1)

        return {
            "match": f"{match_data['home']} vs {match_data['away']}",
            "expert_consensus": {"1": p1, "X": px, "2": p2},
            "recommended_bet": label,
            "bankroll_management": {
                "kelly_fraction": f"{round(max(0, kelly) * 100 * fraction, 2)}%",
                "edge": f"{round((best_prob - (1/odds))*100, 2)}%"
            },
            "params_used": self.params
        }

if __name__ == "__main__":
    system = ExpertFootballSystem()
    test_match = {"home": "Real Madrid", "away": "Barcelona", "h_xg": 2.2, "a_xg": 1.4, "odds": {"1": 2.05, "X": 3.50, "2": 3.80}}
    print(json.dumps(system.run_inference(test_match), indent=2))
