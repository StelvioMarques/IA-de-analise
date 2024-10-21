from flask import Flask, request, jsonify
import os
import cv2

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    # Verifica se a requisição tem o arquivo
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # Salva o vídeo na pasta uploads
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Processar o vídeo
    results = process_video(file_path)

    return jsonify(results)  # Retorna os resultados como JSON para o frontend

def process_video(video_path):
    # Carregar o vídeo
    cap = cv2.VideoCapture(video_path)
    
    frame_count = 0
    total_objects_detected = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Contar o número de frames
        frame_count += 1
        
        # Simular detecção de objetos
        if frame_count % 30 == 0:  # Exemplo: detecta a cada 30 frames
            total_objects_detected += 1
        
    cap.release()
    
    # Armazenar e retornar resultados
    results = {
        'frame_count': frame_count,
        'total_objects_detected': total_objects_detected,
    }

    return results  # Retorna os resultados como dicionário

if __name__ == '__main__':
    app.run(debug=True)
