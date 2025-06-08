from flask import Flask, request, jsonify, render_template_string
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
def show_latest_map():
    if not locations:
        return "No locations received yet."

    latest = locations[-1]
    lat = latest.get("latitude", 0)
    lon = latest.get("longitude", 0)

    map_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Latest Location</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
        <style>#map {{ height: 100vh; }}</style>
    </head>
    <body>
        <div id="map"></div>
        <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
        <script>
            const lat = {lat};
            const lon = {lon};
            const map = L.map('map').setView([lat, lon], 15);
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                attribution: '&copy; OpenStreetMap contributors'
            }}).addTo(map);
            L.marker([lat, lon]).addTo(map)
                .bindPopup('📍 Most Recent Location')
                .openPopup();
        </script>
    </body>
    </html>
    """
    return render_template_string(map_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
