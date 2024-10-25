from flask import Flask, request, jsonify, render_template, url_for
from algorithm import compare_melodies

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

        # Сохраняем временные файлы для обработки
        file1.save('temp1.mp3')
        file2.save('temp2.mp3')

        file_path1 = '/Users/sarafanovnikita/Desktop/Sound Comparin(clean)/temp1.mp3'
        file_path2 = '/Users/sarafanovnikita/Desktop/Sound Comparin(clean)/temp2.mp3'
        index = round(compare_melodies(file_path1, file_path2), 2)
        
        return jsonify({"difference": index})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)