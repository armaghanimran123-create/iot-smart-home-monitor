from flask import Flask, render_template, jsonify
import random

# THis is the UART Configuration 
# To enable real hardware mode, install pyserial and connect the inverter:
#   pip install pyserial
# Then set UART_PORT to the correct port:
#   Raspberry Pi (Linux): '/dev/ttyUSB0' or '/dev/ttyAMA0'
#   Windows:              'COM3' (check Device Manager)
# Expected inverter CSV format over UART (9600 baud):
#   outputVoltage,inputVoltage,batteryVoltage,loadPercent,overload,batteryLow,overTemp
#   Example: 228,415,49,73,0,0,1

UART_PORT = '/dev/ttyUSB0'
UART_BAUD = 9600

# Try to connect to UART on startup. Falls back to simulation if unavailable.
try:
    import serial
    ser = serial.Serial(UART_PORT, baudrate=UART_BAUD, timeout=1)
    SIMULATION_MODE = False
    print(f"Connected to inverter on {UART_PORT} at {UART_BAUD} baud.")
except Exception:
    ser = None
    SIMULATION_MODE = True
    print("UART not available. Running in Simulation Mode.")

app = Flask(__name__)

def read_uart():
    """Read and parse one CSV line from the inverter over UART."""
    try:
        raw = ser.readline().decode('utf-8').strip()
        values = raw.split(',')
        if len(values) != 7:
            raise ValueError(f"Unexpected format: {raw}")
        return {
            "outputVoltage":  values[0],
            "inputVoltage":   values[1],
            "batteryVoltage": values[2],
            "loadPercent":    values[3],
            "overload":       values[4] == '1',
            "batteryLow":     values[5] == '1',
            "overTemperature": values[6] == '1'
        }
    except Exception as e:
        print(f"UART read error: {e}. Falling back to simulation for this frame.")
        return simulate()

def simulate():
    """Generate realistic synthetic inverter data for testing."""
    return {
        "outputVoltage":  str(random.randint(210, 230)),
        "inputVoltage":   str(random.randint(380, 420)),
        "batteryVoltage": str(random.randint(48, 52)),
        "loadPercent":    str(random.randint(0, 100)),
        "overload":       random.choice([True, False]),
        "batteryLow":     random.choice([True, False]),
        "overTemperature": random.choice([True, False])
    }

@app.route('/')
def index():
    return render_template('panel_view.html')

@app.route('/api/inverterdata')
def inverterdata():
    if SIMULATION_MODE:
        data = simulate()
    else:
        data = read_uart()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
