# Import necessary libraries
from flask import Flask, render_template, jsonify
import socket
import traceback
import requests
import time
import RPi.GPIO as GPIO

# Create a Flask application instance
app = Flask(__name__)


# GPIO setup
GPIO.setmode(GPIO.BOARD)
PIN_TRIGGER = 7
PIN_ECHO = 11
GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)  

def measure_distance():
    GPIO.output(PIN_TRIGGER, GPIO.LOW)
    time.sleep(2)

    GPIO.output(PIN_TRIGGER, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    while GPIO.input(PIN_ECHO) == 0:
        pulse_start_time = time.time()

    while GPIO.input(PIN_ECHO) == 1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)

    return distance

def check_bin_status(distance):
    threshold_distance = 5  # Threshold distance to determine if bin is full
    if distance <= threshold_distance:  # Use <= to include 5 cm as well
        return "Bin is full and should be taken out."
    else:
        return "Bin is not full."


# Route for index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for checking bin status
@app.route('/bin_status')
def bin_status():
    distance = measure_distance()
    status = check_bin_status(distance)
    return jsonify({'distance': distance, 'status': status})

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
