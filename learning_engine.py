import sqlite3
import pandas as pd
import json
import os

def refine_models():
    print("🧠 Optimizando hiperparámetros del sistema experto...")
    conn = sqlite3.connect('football_data.db')
    
    # 1. Analizar desempeño histórico
    try:
        query = "SELECT predicted_result, actual_result FROM predictions WHERE actual_result IS NOT NULL"
        df = pd.read_sql_query(query, conn)
    except:
        df = pd.DataFrame()

    # Parámetros base
    params = {"k_factor": 32, "dynamic_xg_bias": 0.10, "volatility_filter": 0.05}

    if not df.empty:
        accuracy = (df['predicted_result'] == df['actual_result']).mean()
        print(f"📈 Precisión actual: {accuracy:.2%}")

        # 2. Lógica de Sintonización Fina (Fine-tuning)
        if accuracy < 0.55:
            # Aumentar sensibilidad a sorpresas (ELO más agresivo)
            params["k_factor"] = 42
            params["dynamic_xg_bias"] = 0.18
            print("⚠️ Ajuste: Aumentando sensibilidad ante volatilidad de resultados.")
        elif accuracy > 0.75:
            # Mantener estabilidad si el modelo es muy preciso
            params["k_factor"] = 24
            params["dynamic_xg_bias"] = 0.08
            print("✅ Ajuste: Estabilizando parámetros para mantener racha ganadora.")

    # 3. Guardar parámetros para que predict_tool.py los use
    with open('model_params.json', 'w') as f:
        json.dump(params, f, indent=2)
    
    conn.close()
    print("🚀 Parámetros actualizados en model_params.json")

if __name__ == '__main__':
    refine_models()
