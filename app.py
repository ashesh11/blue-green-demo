import os
import pika
import logging
from flask import Flask, make_response

# Create a Flask web app
app = Flask(__name__)

# Configure the logging format and log file path
log_file = 'logs/app.log'

# Set up a logger for your Flask app
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')

# Create a file handler for the logger
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Retrieve RabbitMQ connection parameters from environment variables
rabbitmq_host = os.environ.get('RABBITMQ_HOST')
# rabbitmq_port = int(os.environ.get('RABBITMQ_PORT'))


# Define a route for the root URL ("/")
@app.route('/')
def hello_world():
    # Create a connection to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=rabbitmq_host,
    ))
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue='message-queue')

    message = f"Hello, {os.environ.get('ENV')} World!"
    response = make_response(message)
    logger.info(message)
    channel.basic_publish(exchange='', routing_key='message-queue', body=f'Message in {rabbitmq_host}.')
    return response

# Run the app if this script is executed
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
