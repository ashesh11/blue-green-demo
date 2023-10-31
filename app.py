import os
from flask import Flask

# Create a Flask web app
app = Flask(__name__)

# Define a route for the root URL ("/")
@app.route('/')
def hello_world():
    return f"Hello, {os.environ.get('ENV')} World!"

# Run the app if this script is executed
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
