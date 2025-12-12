<template>
  <div class="map-container">
    <div id="map" ref="mapRef"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const props = defineProps({
  markers: {
    type: Array,
    default: () => []
  },
  readOnly: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['marker-click']);

const mapRef = ref(null);
let map = null;
const markerLayers = [];

onMounted(() => {
  // Inicializar mapa
  map = L.map(mapRef.value).setView([40.416, -3.703], 3);

  // Añadir tiles de OpenStreetMap
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);

  // Renderizar marcadores iniciales
  renderMarkers();
});

// Observar cambios en los marcadores
watch(() => props.markers, () => {
  renderMarkers();
}, { deep: true });

function renderMarkers() {
  if (!map) return;

  // Limpiar marcadores anteriores
  markerLayers.forEach(marker => map.removeLayer(marker));
  markerLayers.length = 0;

  // Añadir nuevos marcadores
  props.markers.forEach(markerData => {
    // Construir contenido del popup
    let popupContent = `<div class="marker-popup">
      <strong>${markerData.place_name}</strong><br>`;
    
    if (markerData.image_url) {
      popupContent += `<img src="${markerData.image_url}" alt="${markerData.place_name}" class="popup-image"><br>`;
    }
    
    // Solo mostrar botón de eliminar si NO es modo solo lectura
    if (!props.readOnly) {
      popupContent += `<button class="delete-btn" onclick="window.deleteMarker('${markerData.id}')">Eliminar</button>`;
    }
    
    popupContent += `</div>`;

    const marker = L.marker([markerData.latitude, markerData.longitude])
      .addTo(map)
      .bindPopup(popupContent, { maxWidth: 300 });
    
    markerLayers.push(marker);
  });

  // Ajustar vista si hay marcadores
  if (props.markers.length > 0) {
    const bounds = L.latLngBounds(props.markers.map(m => [m.latitude, m.longitude]));
    map.fitBounds(bounds, { padding: [50, 50] });
  }
}

// Exponer función para eliminar marcador desde el popup
window.deleteMarker = (id) => {
  emit('marker-click', id);
};
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 500px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

#map {
  width: 100%;
  height: 100%;
}

:deep(.marker-popup) {
  text-align: center;
}

:deep(.popup-image) {
  width: 100%;
  max-width: 280px;
  height: 150px;
  object-fit: cover;
  border-radius: 6px;
  margin: 8px 0;
}

:deep(.delete-btn) {
  background: #ef4444;
  color: white;
  border: none;
  padding: 6px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  margin-top: 4px;
  font-weight: 500;
}

:deep(.delete-btn:hover) {
  background: #dc2626;
}
</style>
