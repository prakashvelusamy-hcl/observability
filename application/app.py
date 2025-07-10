import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL
from prometheus_flask_exporter import PrometheusMetrics
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logging.info("Setting LOGLEVEL to INFO")

# Initialize Flask app
app = Flask(__name__)

# Configure MySQL from environment variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'default_user')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'default_password')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'default_db')

# Initialize MySQL
mysql = MySQL(app)

# Initialize Prometheus metrics exporter
metrics = PrometheusMetrics(app)

# Explicitly set /metrics route if necessary
@app.route('/metrics')
def metrics_route():
    return metrics.generate_latest()

# Add information about the app for Prometheus
metrics.info("app_info", "App Info, this can be anything you want", version="1.0.0")

# Route for the home page
@app.route('/')
def hello():
    # Retrieve messages from the database
    cur = mysql.connection.cursor()
    cur.execute('SELECT message FROM messages')
    messages = cur.fetchall()
    cur.close()
    return render_template('index.html', messages=messages)

# Route to submit new messages
@app.route('/submit', methods=['POST'])
def submit():
    new_message = request.form.get('new_message')
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('hello'))

# Route to say hello (optional - for testing)
@app.route("/flask-prometheus-grafana-example/")
def say_hello():
    return jsonify({"message": "hello"})

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
