<template>
  <div class="add-place-form">
    <h3>Añadir nuevo lugar visitado</h3>
    
    <div class="form-group">
      <label for="search">Buscar ciudad o país:</label>
      <input
        id="search"
        v-model="searchQuery"
        @input="onSearchInput"
        type="text"
        placeholder="Ej: Madrid, España"
        class="input-field"
      />
    </div>

    <div v-if="searchResults.length > 0" class="search-results">
      <div
        v-for="result in searchResults"
        :key="result.place_id"
        @click="selectPlace(result)"
        class="search-result-item"
      >
        <strong>{{ result.display_name }}</strong>
      </div>
    </div>

    <div v-if="selectedPlace" class="selected-section">
      <div class="selected-place">
        <p><strong>Lugar seleccionado:</strong> {{ selectedPlace.display_name }}</p>
        <p><strong>Coordenadas:</strong> {{ selectedPlace.lat }}, {{ selectedPlace.lon }}</p>
      </div>

      <ImageUpload 
        @image-uploaded="handleImageUploaded"
        @image-removed="handleImageRemoved"
      />

      <button @click="addMarker" class="btn-add" :disabled="loading">
        {{ loading ? 'Añadiendo...' : 'Añadir al mapa' }}
      </button>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { geocodingService } from '../services/marker';
import ImageUpload from './ImageUpload.vue';

const emit = defineEmits(['place-added']);

const searchQuery = ref('');
const searchResults = ref([]);
const selectedPlace = ref(null);
const imageUrl = ref('');
const loading = ref(false);
const error = ref('');

let debounceTimer = null;

function onSearchInput() {
  error.value = '';
  selectedPlace.value = null;
  imageUrl.value = '';
  
  // Implementar debounce para respetar límites de Nominatim
  clearTimeout(debounceTimer);
  
  if (searchQuery.value.length < 3) {
    searchResults.value = [];
    return;
  }

  debounceTimer = setTimeout(async () => {
    try {
      const results = await geocodingService.searchPlace(searchQuery.value);
      searchResults.value = results;
    } catch (err) {
      error.value = 'Error al buscar lugares. Intenta de nuevo.';
      console.error(err);
    }
  }, 1000); // Esperar 1 segundo después del último cambio
}

function selectPlace(result) {
  selectedPlace.value = result;
  searchResults.value = [];
  imageUrl.value = '';
}

function handleImageUploaded(url) {
  imageUrl.value = url;
}

function handleImageRemoved() {
  imageUrl.value = '';
}

async function addMarker() {
  if (!selectedPlace.value) return;

  loading.value = true;
  error.value = '';

  try {
    const markerData = {
      place_name: selectedPlace.value.display_name,
      latitude: parseFloat(selectedPlace.value.lat),
      longitude: parseFloat(selectedPlace.value.lon),
      image_url: imageUrl.value || null
    };

    emit('place-added', markerData);
    
    // Resetear formulario
    searchQuery.value = '';
    selectedPlace.value = null;
    imageUrl.value = '';
  } catch (err) {
    error.value = 'Error al añadir el lugar. Intenta de nuevo.';
    console.error(err);
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.add-place-form {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h3 {
  margin: 0 0 20px 0;
  font-size: 20px;
  font-weight: 600;
  color: #111827;
}

.form-group {
  margin-bottom: 16px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.input-field {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  box-sizing: border-box;
}

.input-field:focus {
  outline: none;
  border-color: #3b82f6;
}

.search-resection {
  margin-top: 16px;
}

.selected-place {
  padding: 16px;
  background: #f0f9ff;
  border-radius: 6px;
  border: 1px solid #bfdbfe;
  margin-bottom: 16px
}

.search-result-item {
  padding: 12px;
  cursor: pointer;
  border-bottom: 1px solid #e5e7eb;
}

.search-result-item:last-child {
  border-bottom: none;
}

.search-result-item:hover {
  background: #f3f4f6;
}

.selected-place {
  margin-top: 16px;
  padding: 16px;
  background: #f0f9ff;
  border-radius: 6px;
  border: 1px solid #bfdbfe;
}

.selected-place p {
  margin: 4px 0;
  font-size: 14px;
  color: #1e40af;
}

.btn-add {
  margin-top: 12px;
  width: 100%;
  padding: 12px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}

.btn-add:hover:not(:disabled) {
  background: #2563eb;
}

.btn-add:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.error-message {
  margin-top: 12px;
  padding: 12px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 6px;
  color: #dc2626;
  font-size: 14px;
}
</style>
