from flask import Flask, request, jsonify, render_template
from algorithm import compare_melodies
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare_files():
    try:
        # Получаем файлы из запроса
        if 'file1' not in request.files or 'file2' not in request.files:
            return jsonify({"error": "Оба аудиофайла должны быть предоставлены"}), 400

        file1 = request.files['file1']
        file2 = request.files['file2']

        # Читаем файлы в память
        file1_bytes = io.BytesIO(file1.read())
        file2_bytes = io.BytesIO(file2.read())

        # Передаем байтовые потоки в функцию сравнения мелодий
        index = compare_melodies(file1_bytes, file2_bytes)
        
        return jsonify({"difference": index})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)