from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def upload_page():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    tosca_file = request.files.get('tosca_file')
    provider = request.form.get('provider')
    return f'File received: {tosca_file.filename} | Provider: {provider}'

if __name__ == '__main__':
    app.run(debug=True)