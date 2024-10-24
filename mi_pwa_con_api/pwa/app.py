from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Ruta para el index de la PWA
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para el archivo manifest.json
@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

# Ruta para el service worker
@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('static', 'service-worker.js')

if __name__ == '__main__':
    app.run(debug=True)
