from flask import Flask, request, render_template, send_from_directory
import os
import face_recognition

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads')

# Pastikan direktori uploads ada
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def compare_images(image_path1, image_path2):
    image1 = face_recognition.load_image_file(image_path1)
    image2 = face_recognition.load_image_file(image_path2)

    face_encoding1 = face_recognition.face_encodings(image1)[0]
    face_encoding2 = face_recognition.face_encodings(image2)[0]

    results = face_recognition.compare_faces([face_encoding1], face_encoding2)

    return "The faces match." if results[0] else "The faces do not match."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']

        image_path1 = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        image_path2 = os.path.join(app.config['UPLOAD_FOLDER'], file2.filename)
        file1.save(image_path1)
        file2.save(image_path2)

        result = compare_images(image_path1, image_path2)
        return render_template('result.html', result=result, image1=file1.filename, image2=file2.filename)

    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

