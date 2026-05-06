from flask import Flask, render_template_string
import os

app = Flask(__name__)

@app.route('/')
def home():
    index_path = "/var/www/html/index.html"
    if os.path.exists(index_path):
        with open(index_path, 'r') as f:
            content = f.read()
        return render_template_string(content)
    return "Vulnerable Web App Running", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
