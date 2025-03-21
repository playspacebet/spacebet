from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Serve static files from the static directory
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Route for the main page
@app.route('/')
def index():
    return render_template('main.html')

# Catch-all route for other paths
@app.route('/<path:path>')
def catch_all(path):
    # Try to serve it as a template if it exists
    if os.path.exists(f'templates/{path}'):
        return render_template(path)
    # Otherwise return the main page (for SPA routing)
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)