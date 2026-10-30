# Velora — Move & Stay

A Flask demo app combining ride booking and accommodation listings.

## Features
- Sign up, log in, and log out
- Password hashing with Werkzeug
- SQLite accounts and booking history
- Ride booking demo with three ride categories
- Sample accommodation listings and booking flow
- Real interactive Leaflet map using OpenStreetMap tiles
- Browser geolocation to show the user's current position

## Run locally
Requires Python 3.10+ and an internet connection for map tiles and Google Fonts.

```powershell
# Windows PowerShell / Command Prompt
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
py app.py
```
Open http://127.0.0.1:5000 in your browser.

## Live map
The map is interactive and uses OpenStreetMap tiles with Leaflet; it is not a static image. Allow browser location permission to show your current position. Geolocation generally requires localhost or HTTPS. If permission is denied, the map still opens around Abuja.

## Demo limitations
Ride fares and stay listings are illustrative. Bookings are saved locally; there is no real driver dispatch, payment processing, host inventory, or third-party booking integration. Before deployment, set a strong SECRET_KEY, disable Flask debug mode, add CSRF protection, validate bookings, and use HTTPS.
