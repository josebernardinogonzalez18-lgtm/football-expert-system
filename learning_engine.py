import sqlite3
import pandas as pd
import requests
import os

def refine_models():
    print("🧠 Iniciando fase de auto-aprendizaje y optimización...")
    conn = sqlite3.connect('football_data.db')
    
    # 1. Obtener predicciones pendientes de validación
    # Simulamos la carga de resultados reales desde la API para el cierre del día
    query = "SELECT match_name, predicted_result, actual_result FROM predictions WHERE actual_result IS NOT NULL"
    df = pd.read_sql_query(query, conn)
    
    if df.empty:
        print("ℹ️ No hay suficientes datos nuevos para ajustar los modelos hoy.")
        return

    # 2. Calcular tasa de error
    accuracy = (df['predicted_result'] == df['actual_result']).mean()
    print(f"📈 Precisión de la última jornada: {accuracy:.2%}")

    # 3. Lógica de Ajuste: Si la precisión baja del 60%, incrementamos la penalización por fatiga
    # y ajustamos el factor K del sistema ELO
    if accuracy < 0.60:
        print("⚠️ Rendimiento bajo. Ajustando hiperparámetros de Poisson...")
        # Aquí el script modificaría un archivo de configuración 'model_params.json'
        with open('model_params.json', 'w') as f:
            json.dump({"k_factor": 48, "dynamic_xg_bias": 0.15}, f)
    else:
        print("✅ El modelo mantiene un rendimiento óptimo.")

    conn.close()

if __name__ == '__main__':
    refine_models()
