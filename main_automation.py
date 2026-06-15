import os
import json
from predict_tool import RealTimeExpertSystem
# Importamos las funciones de los otros módulos creados previamente
from validate_tool import validate_and_save
import sqlite3

def run_daily_automation():
    print("🚀 Iniciando Ciclo de Automatización Diaria...")
    api_key = os.environ.get('ALLSPORTS_API_KEY', '2745fc3b554dbf9f541f8b1adf111d78d76ef56b01fe02c7f1d2f2313d2fe5bf')
    
    # 1. Inicializar Sistema
    system = RealTimeExpertSystem(api_key)
    
    # 2. Obtener y Analizar Partidos Reales
    print("📡 Obteniendo datos de la API...")
    report = system.analyze_real_data()
    
    if not report:
        print("⚠️ No hay partidos para analizar hoy.")
        return

    # 3. Guardar Predicciones en la DB Local para seguimiento
    print(f"📊 Analizados {len(report)} partidos. Guardando resultados...")
    
    # Generar un archivo de log diario para GitHub Artifacts
    with open('daily_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("✅ Ciclo completado con éxito. Reporte generado en daily_report.json")

if __name__ == '__main__':
    run_daily_automation()
