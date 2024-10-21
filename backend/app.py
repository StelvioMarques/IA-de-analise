from flask import Flask, request, jsonify
import cv2
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({"error": "No file part"}), 400

    video_file = request.files['video']
    if video_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Salvar o vídeo
    video_path = os.path.join('uploads', video_file.filename)
    video_file.save(video_path)

    # Processar o vídeo com OpenCV
    process_video(video_path)

    return jsonify({"message": "Video processed successfully!"})

def process_video(video_path):
    # Lógica para processar o vídeo usando OpenCV
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Exemplo de processamento: converter para escala de cinza
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Aqui, poderíamos aplicar algoritmos para análise de condução
        # Exibir o frame processado (opcional)
        cv2.imshow('Video', gray_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
