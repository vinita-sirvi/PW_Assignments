from flask import Flask, render_template, request
import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)

# Ensure the 'logs' directory exists
if not os.path.exists('logs'):
    os.mkdir('logs')

# Configure logging
handler = RotatingFileHandler('logs/app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

@app.route('/')
def home():
    return "Welcome to the Home Page"

@app.route('/trigger_error')
def trigger_error():
    # This route deliberately raises an exception to demonstrate 500 error handling
    raise Exception("This is a deliberate exception")

@app.errorhandler(404)
def not_found_error(error):
    app.logger.error('Page not found: %s', (request.path))
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error('Server Error: %s', (error))
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)