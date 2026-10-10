from flask import Flask, render_template, render_template_string

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/sos")
def sos():
    return render_template("sos.html")


@app.route("/location")
def location():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>My Location | WomenSafe</title>
      <style>
        body { font-family: Arial; background:#fff5f8; padding:20px; }
        main { max-width:520px; margin:30px auto; background:white;
               padding:25px; border-radius:18px; text-align:center; }
        h1 { color:#8e2457; }
        button, .btn { display:block; width:100%; box-sizing:border-box;
          padding:14px; margin-top:14px; border:0; border-radius:9px;
          background:#8e2457; color:white; text-decoration:none;
          font-size:16px; cursor:pointer; }
        #status { overflow-wrap:anywhere; line-height:1.6; }
      </style>
    </head>
    <body>
      <main>
        <h1>📍 My Location</h1>
        <p>Press the button and allow location permission to get your location.</p>
        <button onclick="getLocation()">Get My Location</button>
        <p id="status" role="status" aria-live="polite">Location not requested yet.</p>
        <a id="map" class="btn" href="#" target="_blank" rel="noopener" hidden>
          Open in Google Maps
        </a>
        <button id="share" onclick="shareLocation()" hidden>Share Location</button>
        <p><a href="/">← Back to Home</a></p>
      </main>
      <script>
        let locationUrl = "";

        function getLocation() {
          const status = document.getElementById("status");
          if (!navigator.geolocation) {
            status.textContent = "Your browser does not support location.";
            return;
          }

          status.textContent = "Requesting location permission...";
          navigator.geolocation.getCurrentPosition(
            function(pos) {
              locationUrl = "https://maps.google.com/?q=" +
                pos.coords.latitude + "," + pos.coords.longitude;
              status.textContent = "Location found. You can open or share the map link.";
              document.getElementById("map").href = locationUrl;
              document.getElementById("map").hidden = false;
              document.getElementById("share").hidden = false;
            },
            function() {
              status.textContent = "Location unavailable. Allow permission and try again.";
            },
            {enableHighAccuracy:true, timeout:15000, maximumAge:0}
          );
        }

        async function shareLocation() {
          if (!locationUrl) return;
          try {
            if (navigator.share) {
              await navigator.share({title:"My location", url:locationUrl});
            } else if (navigator.clipboard) {
              await navigator.clipboard.writeText(locationUrl);
              document.getElementById("status").textContent =
                "Map link copied. Paste it into a message to share.";
            } else {
              window.prompt("Copy this location link:", locationUrl);
            }
          } catch (error) {
            if (error.name !== "AbortError") {
              document.getElementById("status").textContent =
                "Sharing was not completed. Open the map link and share it manually.";
            }
          }
        }
      </script>
    </body>
    </html>
    """)


@app.route("/contacts")
def contacts():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Emergency Contacts | WomenSafe</title>
      <style>
        body { font-family:Arial; background:#fff5f8; padding:20px; }
        main { max-width:520px; margin:30px auto; background:white;
               padding:25px; border-radius:18px; }
        h1 { color:#8e2457; text-align:center; }
        label { display:block; margin-top:18px; font-weight:bold; }
        input { box-sizing:border-box; width:100%; padding:13px;
                margin-top:8px; border:1px solid #ccc; border-radius:8px;
                font-size:16px; }
        button, .btn { display:block; box-sizing:border-box; width:100%;
          padding:13px; margin-top:14px; border:0; border-radius:9px;
          background:#8e2457; color:white; text-align:center;
          text-decoration:none; font-size:16px; cursor:pointer; }
        #status { line-height:1.5; overflow-wrap:anywhere; }
      </style>
    </head>
    <body>
      <main>
        <h1>👥 Emergency Contacts</h1>
        <p>Save one trusted contact on this device. The number is stored in this browser only.</p>
        <label for="phone">Trusted contact phone number</label>
        <input id="phone" type="tel" placeholder="Enter phone number"
               autocomplete="tel" maxlength="20">
        <button onclick="saveContact()">Save Contact</button>
        <button onclick="deleteContact()">Remove Saved Contact</button>
        <p id="status" role="status" aria-live="polite"></p>
        <a class="btn" href="/sos">Go to SOS Alert</a>
        <p style="text-align:center"><a href="/">← Back to Home</a></p>
      </main>
      <script>
        const phoneInput = document.getElementById("phone");
        const status = document.getElementById("status");

        try {
          phoneInput.value = localStorage.getItem("womensafe_contact") || "";
        } catch (error) {
          status.textContent = "Browser storage is unavailable. Enter the number on the SOS page instead.";
        }

        function saveContact() {
          const phone = phoneInput.value.trim();
          if (!phone || !/[0-9]{7,15}/.test(phone.replace(/\\D/g, ""))) {
            status.textContent = "Enter a valid contact number.";
            return;
          }
          try {
            localStorage.setItem("womensafe_contact", phone);
            status.textContent = "Contact saved on this device.";
          } catch (error) {
            status.textContent = "Could not save. Enter the number directly on the SOS page.";
          }
        }

        function deleteContact() {
          try { localStorage.removeItem("womensafe_contact"); } catch (error) {}
          phoneInput.value = "";
          status.textContent = "Saved contact removed from this browser.";
        }
      </script>
    </body>
    </html>
    """)


@app.route("/help")
def help_page():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Emergency Help | WomenSafe</title>
    </head>
    <body style="font-family:Arial;text-align:center;background:#fff5f8;padding:25px">
      <h1>🆘 Emergency Help</h1>
      <h2>Emergency number: 112</h2>
      <p><a href="tel:112">Call 112</a></p>
      <h2>Women Helpline: 181</h2>
      <p><a href="tel:181">Call 181</a></p>
      <h2>Ambulance: 108</h2>
      <p><a href="tel:108">Call 108</a></p>
      <p><a href="/">← Back to Home</a></p>
    </body>
    </html>
    """)


@app.route("/safety-tips")
def safety_tips():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Safety Tips | WomenSafe</title>
    </head>
    <body style="font-family:Arial;background:#fff5f8;padding:25px">
      <h1>💡 Women Safety Tips</h1>
      <ul>
        <li>Tell a trusted person where you are going.</li>
        <li>Keep your phone charged when travelling.</li>
        <li>Use trusted transport when possible.</li>
        <li>Share your location only with people you trust.</li>
        <li>If you are in immediate danger in India, call 112.</li>
      </ul>
      <a href="/">← Back to Home</a>
    </body>
    </html>
    """)


if __name__ == "__main__":
    app.run(debug=True)
