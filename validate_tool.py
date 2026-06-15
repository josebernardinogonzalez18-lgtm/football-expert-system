import json
import sqlite3

def validate_and_save(predictions, actual_results):
    conn = sqlite3.connect('football_data.db')
    cursor = conn.cursor()
    
    report = []
    correct = 0
    
    for pred in predictions:
        match_name = pred['match']
        actual = actual_results.get(match_name)
        is_correct = pred['prediction'] == actual
        if is_correct: correct += 1
        
        # Guardar en base de datos
        cursor.execute('''
            INSERT INTO predictions (match_name, predicted_result, confidence, actual_result)
            VALUES (?, ?, ?, ?)
        ''', (match_name, pred['prediction'], pred.get('confidence', 'N/A'), actual))
        
        report.append({
            "match": match_name,
            "success": is_correct,
            "details": f"Pred: {pred['prediction']} | Real: {actual}"
        })
    
    conn.commit()
    conn.close()
    
    accuracy = (correct / len(predictions)) * 100 if predictions else 0
    return {"accuracy": f"{accuracy}%", "saved_to_db": True, "results": report}

if __name__ == "__main__":
    # Simulación de prueba
    test_preds = [{"match": "Real Madrid vs Barcelona", "prediction": "Home Win", "confidence": "65%"}]
    test_actual = {"Real Madrid vs Barcelona": "Home Win"}
    print(json.dumps(validate_and_save(test_preds, test_actual), indent=2))
