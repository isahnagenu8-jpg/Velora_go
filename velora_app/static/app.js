// Leaflet + OpenStreetMap render a real interactive map (not an image).
const mapEl = document.getElementById('map');
if (mapEl && window.L) {
  const map = L.map('map').setView([9.0765, 7.3986], 12); // Abuja fallback
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map);
  L.control.zoom({position:'bottomright'}).addTo(map);
  let marker, circle;
  const status = document.getElementById('locationStatus');
  function locate() {
    if (!navigator.geolocation) { status.textContent = "Location isn't supported by this browser."; return; }
    status.textContent = 'Finding your location…';
    navigator.geolocation.getCurrentPosition(pos => {
      const {latitude:lat, longitude:lng, accuracy} = pos.coords;
      map.setView([lat,lng], 16);
      if (marker) map.removeLayer(marker); if (circle) map.removeLayer(circle);
      marker = L.circleMarker([lat,lng], {radius:9,color:'#fff',weight:4,fillColor:'#6558f5',fillOpacity:1}).addTo(map).bindPopup('<b>You are here</b><br>Your current location');
      circle = L.circle([lat,lng], {radius:Math.max(accuracy,35),color:'#6558f5',weight:1,fillColor:'#6558f5',fillOpacity:.09}).addTo(map);
      status.textContent = 'Your current location is on the map.';
      const pickup = document.getElementById('pickup'); if (pickup && !pickup.value) pickup.value = `${lat.toFixed(5)}, ${lng.toFixed(5)}`;
    }, err => { status.textContent = ({1:'Location permission denied. The map still works.',2:'Location unavailable. Try again.',3:'Location request timed out. Try again.'})[err.code] || "Couldn't get your location."; }, {enableHighAccuracy:true,timeout:12000,maximumAge:30000});
  }
  document.getElementById('useLocation')?.addEventListener('click', locate);
  document.getElementById('mapLocate')?.addEventListener('click', locate);
  setTimeout(() => map.invalidateSize(), 250); locate();
}
async function saveBooking(payload) {
  const response = await fetch('/book', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
  if (response.redirected) { window.location.href = response.url; return; }
  const result = await response.json(); if (!response.ok) throw new Error(result.message || 'Booking failed.');
  alert(result.message); window.location.href = '/dashboard';
}
document.getElementById('rideForm')?.addEventListener('submit', async e => {
  e.preventDefault(); const pickup = document.getElementById('pickup').value.trim(); const dropoff = document.getElementById('dropoff').value.trim();
  const ride = document.querySelector('input[name="rideType"]:checked').value;
  const fares = {'Velora Go':'From ₦2,500','Velora Comfort':'From ₦3,800','Velora XL':'From ₦5,200'};
  try { await saveBooking({kind:'ride',title:ride,details:`${pickup} → ${dropoff}`,price:fares[ride]}); } catch(err) { alert(err.message); }
});
document.querySelectorAll('.book-stay').forEach(button => button.addEventListener('click', async () => {
  try { await saveBooking({kind:'stay',title:button.dataset.title,details:button.dataset.details,price:button.dataset.price}); } catch(err) { alert(err.message); }
}));
document.querySelectorAll('.ride-option').forEach(option => option.addEventListener('click', () => { document.querySelectorAll('.ride-option').forEach(x=>x.classList.remove('selected')); option.classList.add('selected'); option.querySelector('input').checked=true; }));
document.querySelectorAll('.stay-heart').forEach(heart => heart.addEventListener('click', () => heart.classList.toggle('hearted')));
