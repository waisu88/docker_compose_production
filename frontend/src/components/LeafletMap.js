// LeafletMap.js
import React, { useEffect } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css'


const LeafletMap = () => {
  useEffect(() => {
    const map = L.map('map').setView([52.2, 19.5], 6);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    // Clean up function to remove the map when the component unmounts
    return () => {
      map.remove();
    };
  }, []); // Empty dependency array ensures the effect runs only once after initial render

  
  
  return (
    <div id="map" style={{ height: '500px', width: '500px'}}></div>
  );
};

export default LeafletMap;