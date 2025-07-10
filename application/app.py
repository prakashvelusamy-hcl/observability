import os
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from prometheus_flask_exporter import PrometheusMetrics  # Import the exporter

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

# Create a custom metric to count the number of orders created
# This is a counter metric that will track the number of API calls to '/api/orders'
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
def submit():
    new_message = request.form.get('new_message')
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
    mysql.connection.commit()
    cur.close()

    # Increment the order created counter whenever an order is submitted
    order_created_counter.inc()

    return redirect(url_for('hello'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
