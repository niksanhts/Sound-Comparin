import logging
from flask import Flask, request, jsonify, render_template
from algorithm import compare_melodies
import io

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s') 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare_files():
    try:
        if 'file1' not in request.files or 'file2' not in request.files:
            logging.warning("Оба аудиофайла должны быть предоставлены")
            return jsonify({"error": "Оба аудиофайла должны быть предоставлены"}), 400

        file1 = request.files['file1']
        file2 = request.files['file2']

        file1_bytes = io.BytesIO(file1.read())
        file2_bytes = io.BytesIO(file2.read())

        logging.info("Сравнение файлов начато")
        result = compare_melodies(file1_bytes, file2_bytes)

        if result is None:
            logging.error("Ошибка при сравнении файлов: результат равен None")
            return jsonify({"error": "Ошибка при сравнении файлов"}), 500

        integral_indicator, rhythm, height, volume1, volume2 = result
        
        return jsonify({
            "integral_indicator": integral_indicator,
            "rhythm": rhythm,
            "height": height,
            "volume1": volume1,
            "volume2": volume2
        })

    except Exception as e:
       logging.exception("Произошла ошибка: %s", str(e))
       return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)
