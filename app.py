
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/help")
def help_page():
    return """
    <html>
    <head><title>WomenSafe Help</title></head>
    <body style="font-family:Arial;text-align:center;background:#fff5f8;padding:30px">
        <h1>🆘 Emergency Help</h1>
        <h2>🚔 Police / Emergency: 112</h2>
        <p><a href="tel:112">Call 112</a></p>
        <h2>👩 Women Helpline: 181</h2>
        <p><a href="tel:181">Call 181</a></p>
        <h2>🚑 Ambulance: 108</h2>
        <p><a href="tel:108">Call 108</a></p>
        <a href="/">Back to Home</a>
    </body>
    </html>
    """

@app.route("/sos")
def sos():
    return """
    <h1>🆘 Emergency SOS</h1>
    <p>If you are in immediate danger, call 112.</p>
    <a href="tel:112">Call Emergency Services</a><br><br>
    <a href="/">Back to Home</a>
    """

@app.route("/location")
def location():
    return """
    <h1>📍 My Location</h1>
    <button onclick="getLocation()">Show My Location</button>
    <p id="result"></p>
    <script>
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(pos) {
                    const lat = pos.coords.latitude;
                    const lon = pos.coords.longitude;
                    document.getElementById("result").innerHTML =
                        "Latitude: " + lat + "<br>Longitude: " + lon +
                        '<br><a target="_blank" href="https://maps.google.com/?q=' +
                        lat + ',' + lon + '">Open in Google Maps</a>';
                },
                function() {
                    document.getElementById("result").innerText =
                        "Location permission denied or unavailable.";
                }
            );
        } else {
            document.getElementById("result").innerText =
                "Geolocation is not supported.";
        }
    }
    </script>
    <br><a href="/">Back to Home</a>
    """

@app.route("/contacts")
def contacts():
    return """
    <h1>👥 Emergency Contacts</h1>
    <p>Save trusted contacts in your phone for quick access.</p>
    <a href="tel:112">Call Emergency Services: 112</a><br><br>
    <a href="/">Back to Home</a>
    """

@app.route("/safety-tips")
def safety_tips():
    return """
    <h1>💡 Women Safety Tips</h1>
    <ul>
        <li>Share your travel plans with someone you trust.</li>
        <li>Keep your phone charged.</li>
        <li>Use trusted transport when possible.</li>
        <li>In immediate danger, call 112.</li>
    </ul>
    <a href="/">Back to Home</a>
    """

if __name__ == "__main__":
    app.run(debug=True)
