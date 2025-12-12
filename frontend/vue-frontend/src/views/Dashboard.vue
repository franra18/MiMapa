<template>
  <div>
    <nav class="navbar" v-if="user">
      <span class="user-name">{{ user.username }}</span>
      <button @click="logout" class="btn-logout">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
          <polyline points="16 17 21 12 16 7"></polyline>
          <line x1="21" y1="12" x2="9" y2="12"></line>
        </svg>
        Cerrar Sesión
      </button>
    </nav>
    
    <div class="dashboard-container">
      <div v-if="user" class="content">
        <h1>Mis Lugares Visitados</h1>
        <p class="subtitle">{{ user.email }}</p>

        <div class="main-grid">
          <div class="map-section">
            <MapView :markers="markers" @marker-click="handleDeleteMarker" />
          </div>

          <div class="form-section">
            <AddPlaceForm @place-added="handleAddPlace" />
            <VisitUserForm />
          </div>
        </div>

        <div v-if="markers.length > 0" class="gallery-section">
          <h2>Galería de lugares visitados</h2>
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
          <div v-if="markers.filter(m => m.image_url).length === 0" class="no-images">
            No hay imágenes aún. Añade imágenes al crear marcadores.
          </div>
        </div>

        <VisitsList />
      </div>
      <div v-else class="loading">
        Cargando...
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/api';
import { useRouter } from 'vue-router';
import { markerService } from '../services/marker';
import MapView from '../components/MapView.vue';
import AddPlaceForm from '../components/AddPlaceForm.vue';
import VisitUserForm from '../components/VisitUserForm.vue';
import VisitsList from '../components/VisitsList.vue';

const user = ref(null);
const markers = ref([]);
const router = useRouter();

onMounted(async () => {
  try {
    const response = await api.get('/users/me');
    user.value = response.data;
    await loadMarkers();
  } catch (error) {
    console.error("Error al obtener usuario", error);
    logout();
  }
});

async function loadMarkers() {
  try {
    markers.value = await markerService.getAll();
  } catch (error) {
    console.error("Error al cargar marcadores", error);
  }
}

async function handleAddPlace(markerData) {
  try {
    await markerService.create(markerData);
    await loadMarkers();
  } catch (error) {
    console.error("Error al añadir marcador", error);
    alert('Error al añadir el lugar. Intenta de nuevo.');
  }
}

async function handleDeleteMarker(markerId) {
  if (!confirm('¿Estás seguro de que quieres eliminar este marcador?')) {
    return;
  }

  try {
    await markerService.delete(markerId);
    await loadMarkers();
  } catch (error) {
    console.error("Error al eliminar marcador", error);
    alert('Error al eliminar el marcador. Intenta de nuevo.');
  }
}

const logout = () => {
  localStorage.removeItem('token');
  router.push('/');
};
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
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
}

.btn-logout {
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
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
}

.btn-logout:hover {
  background: #f9fafb;
}

.dashboard-container {
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

.main-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}

@media (max-width: 968px) {
  .main-grid {
    grid-template-columns: 1fr;
  }
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

.no-images {
  text-align: center;
  padding: 40px;
  color: #6b7280;
  font-size: 14px;
}

.loading {
  text-align: center;
  padding: 40px;
  font-size: 16px;
  color: #6b7280;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
}
</style>