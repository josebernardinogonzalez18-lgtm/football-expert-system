import os
import json
import sqlite3
from predict_tool import ExpertFootballSystem
from learning_engine import refine_models
# Importamos la función de aprendizaje profundo definida anteriormente
from a1ed17a1 import tournament_deep_learning 

def run_daily_automation():
    print("🚀 Iniciando Ciclo de Automatización Diaria v6.0 (Deep Learning enabled)...")
    api_key = os.environ.get('ALLSPORTS_API_KEY', '2745fc3b554dbf9f541f8b1adf111d78d76ef56b01fe02c7f1d2f2313d2fe5bf')
    
    # 1. Fase de Aprendizaje Histórico (Contexto del Torneo)
    # Usamos ID 28 para el Mundial como ejemplo base
    print("🧠 Fase 1: Deep Learning del historial del torneo...")
    try:
        tournament_deep_learning(api_key, 28)
    except Exception as e:
        print(f"⚠️ Error en Deep Learning: {e}")

    # 2. Inicializar Sistema de Predicción
    system = ExpertFootballSystem()

    # 3. Obtener y Analizar Partidos Reales
    print("📡 Fase 2: Obteniendo fixtures y generando inferencia...")
    report = system.analyze_real_data()

    if report:
        with open('daily_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        print(f"✅ Reporte generado para {len(report)} partidos.")
    
    # 4. Refinar modelos basados en el feedback loop
    print("⚙️ Fase 3: Refinando parámetros del modelo...")
    refine_models()

if __name__ == '__main__':
    run_daily_automation()
