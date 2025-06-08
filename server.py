from flask import Flask, request, jsonify
from flask_cors import CORS  # 👈 Add this
from datetime import datetime

app = Flask(__name__)
CORS(app)  # 👈 This allows ALL origins by default (for development)

# Just for demo — store everything in a list
locations = []

@app.route('/location', methods=['POST'])
def receive_location():
    print(">>> /location HIT")
    data = request.get_json(force=True, silent=True)  # force parsing even if headers are bad

    if not data:
        print(">>> NO DATA received or JSON parse failed.")
        return jsonify({'error': 'Invalid or missing JSON'}), 400

    lat = data.get('latitude')
    lon = data.get('longitude')
    timestamp = data.get('timestamp', datetime.utcnow().isoformat())

    if lat is None or lon is None:
        print(">>> Missing lat/lon in data:", data)
        return jsonify({'error': 'Missing lat/lon'}), 400

    point = {
        'latitude': lat,
        'longitude': lon,
        'timestamp': timestamp
    }
    locations.append(point)

    print(f"✅ Received location: {point}")
    return jsonify({'status': 'success'}), 200

@app.route('/')
def home():
    return '''
    <html>
    <body>
      <h2>Test Location Post</h2>
      <button onclick="fetch('https://map-w4ew.onrender.com/location', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({latitude: 12.3456, longitude: 65.4321, timestamp: Date.now()})
        }).then(res => alert('Sent')).catch(e => alert('Fail'))">Send Test</button>
    </body>
    </html>
    '''



@app.route('/locations', methods=['GET'])
def get_locations():
    return jsonify(locations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
