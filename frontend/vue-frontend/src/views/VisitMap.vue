<template>
  <div>
    <nav class="navbar">
      <span class="user-name">Visitando mapa de: {{ visitedEmail }}</span>
      <button @click="goBack" class="btn-back">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M19 12H5"></path>
          <path d="M12 19l-7-7 7-7"></path>
        </svg>
        Volver a mi mapa
      </button>
    </nav>
    
    <div class="visit-container">
      <div v-if="loading" class="loading">
        Cargando mapa...
      </div>

      <div v-else-if="error" class="error-container">
        <div class="error-message">{{ error }}</div>
        <button @click="goBack" class="btn-back-error">Volver</button>
      </div>

      <div v-else class="content">
        <h1>Lugares visitados</h1>
        <p class="subtitle">{{ visitedEmail }}</p>

        <div class="map-section">
          <MapView :markers="markers" :read-only="true" @marker-click="() => {}" />
        </div>

        <div v-if="markers.length === 0" class="no-markers">
          Este usuario aún no ha añadido lugares a su mapa
        </div>

        <div v-if="markers.filter(m => m.image_url).length > 0" class="gallery-section">
          <h2>Galería de lugares</h2>
          <div class="image-gallery">
            <div 
              v-for="marker in markers.filter(m => m.image_url)" 
              :key="marker.id"
              class="gallery-item"
            >
              <img :src="marker.image_url" :alt="marker.place_name">
              <div class="gallery-caption">{{ marker.place_name }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { visitService } from '../services/visit';
import MapView from '../components/MapView.vue';

const route = useRoute();
const router = useRouter();

const visitedEmail = ref(route.params.email);
const markers = ref([]);
const loading = ref(true);
const error = ref('');

onMounted(async () => {
  await loadUserMap();
});

async function loadUserMap() {
  try {
    loading.value = true;
    error.value = '';
    markers.value = await visitService.getUserMarkers(visitedEmail.value);
  } catch (err) {
    console.error('Error al cargar mapa:', err);
    if (err.response?.status === 404) {
      error.value = 'Usuario no encontrado';
    } else {
      error.value = 'Error al cargar el mapa. Intenta de nuevo.';
    }
  } finally {
    loading.value = false;
  }
}

function goBack() {
  router.push('/dashboard');
}
</script>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 32px;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  z-index: 10000;
}

.user-name {
  font-size: 15px;
  font-weight: 500;
  color: #111827;
}

.btn-back, .btn-back-error {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  color: #374151;
  font-size: 14px;
  cursor: pointer;
}

.btn-back:hover, .btn-back-error:hover {
  background: #f9fafb;
}

.visit-container {
  min-height: calc(100vh - 57px);
  background: #fafafa;
  padding: 32px;
}

.content {
  max-width: 1400px;
  margin: 0 auto;
}

h1 {
  margin: 0 0 8px 0;
  font-size: 32px;
  font-weight: 600;
  color: #111827;
}

.subtitle {
  margin: 0 0 32px 0;
  font-size: 16px;
  color: #6b7280;
}

.map-section {
  margin-bottom: 32px;
}

.loading {
  text-align: center;
  padding: 40px;
  font-size: 16px;
  color: #6b7280;
}

.error-container {
  text-align: center;
  padding: 40px;
}

.error-message {
  padding: 12px 24px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 6px;
  color: #dc2626;
  font-size: 14px;
  display: inline-block;
  margin-bottom: 16px;
}

.no-markers {
  text-align: center;
  padding: 40px;
  color: #6b7280;
  font-size: 14px;
}

.gallery-section {
  margin-top: 48px;
}

.gallery-section h2 {
  margin: 0 0 24px 0;
  font-size: 24px;
  font-weight: 600;
  color: #111827;
}

.image-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.gallery-item {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.gallery-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.gallery-item img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  display: block;
}

.gallery-caption {
  padding: 12px;
  background: white;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  text-align: center;
}
</style>
