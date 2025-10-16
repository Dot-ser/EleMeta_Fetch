from flask import Flask, request, jsonify , render_template 
from werkzeug.utils import secure_filename
from metadata import get_image_metadata
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.config['JSON_SORT_KEYS'] = False
try:
    app.jinja_env.policies.setdefault('json.dumps_kwargs', {})['sort_keys'] = False
except Exception:
    pass



@app.route('/', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'GET':
        return render_template('index.html')
    # POST from the form
    if 'image' not in request.files:
        return render_template('index.html', error='No file part'), 400
    file = request.files['image']
    if file.filename == '':
        return render_template('index.html', error='No selected file'), 400
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    metadata = get_image_metadata(file_path)
    os.remove(file_path)  
    return render_template('index.html', metadata=metadata)


if __name__ == '__main__':
    app.run()
