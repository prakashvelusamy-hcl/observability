import os
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from prometheus_flask_exporter import PrometheusMetrics  # Import the exporter
import logging

# Initialize the Flask application
app = Flask(__name__)

# Setup logging for debugging purposes
logging.basicConfig(level=logging.DEBUG)

# Configure MySQL from environment variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'default_user')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'default_password')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'default_db')

# Initialize MySQL
mysql = MySQL(app)

# Initialize Prometheus metrics exporter
metrics = PrometheusMetrics(app)

# Log metric exposure at startup
@app.before_first_request
def before_first_request():
    app.logger.debug("Prometheus metrics exposed at /metrics")

# Create a custom metric to count the number of orders created
order_created_counter = metrics.counter('orders_created_total', 'Total number of orders created')

@app.route('/')
def hello():
    # Retrieve messages from the database
    cur = mysql.connection.cursor()
    cur.execute('SELECT message FROM messages')
    messages = cur.fetchall()
    cur.close()
    return render_template('index.html', messages=messages)

@app.route('/submit', methods=['POST'])
@order_created_counter.count_exceptions()  # This decorator automatically increments the counter
def submit():
    new_message = request.form.get('new_message')
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
    mysql.connection.commit()
    cur.close()

    # The decorator @order_created_counter.count_exceptions() takes care of incrementing the counter
    return redirect(url_for('hello'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
