from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# Route to serve the dashboard
@app.route('/')
def index():
    # UPDATED: We are now rendering the new specific filename
    return render_template('panel_view.html')

# API Route to simulate GESS Inverter Data
@app.route('/api/inverterdata')
def inverterdata():
    # Simulation logic based on your internship report
    data = {
        "inputVoltage": f"{random.randint(380, 420)}",  # DC Bus High
        "outputVoltage": f"{random.randint(210, 230)}", # Standard Grid AC
        "batteryVoltage": f"{random.randint(48, 52)}",   # 48V Battery Bank
        "loadPercent": f"{random.randint(0, 100)}",
        "overload": random.choice([True, False]),
        "batteryLow": random.choice([True, False]),
        "overTemperature": random.choice([True, False])
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)