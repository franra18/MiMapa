<template>
  <div class="visits-list">
    <h2>Visitas recibidas</h2>
    
    <div v-if="loading" class="loading">
      Cargando visitas...
    </div>

    <div v-else-if="visits.length === 0" class="no-visits">
      Aún no has recibido visitas a tu mapa
    </div>

    <div v-else class="visits-container">
      <div v-for="visit in visits" :key="visit.id" class="visit-item">
        <div class="visit-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
        </div>
        <div class="visit-info">
          <div class="visit-email">{{ visit.visitor_email }}</div>
          <div class="visit-details">
            <span class="visit-time">{{ formatDate(visit.timestamp) }}</span>
            <span class="visit-token">Token: {{ visit.visitor_oauth_token }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { visitService } from '../services/visit';

const visits = ref([]);
const loading = ref(true);

onMounted(async () => {
  await loadVisits();
});

async function loadVisits() {
  try {
    loading.value = true;
    visits.value = await visitService.getReceivedVisits();
  } catch (error) {
    console.error('Error al cargar visitas:', error);
  } finally {
    loading.value = false;
  }
}

function formatDate(timestamp) {
  const date = new Date(timestamp);
  // Ajustar +1 hora para España
  date.setHours(date.getHours() + 1);
  
  return date.toLocaleString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}
</script>

<style scoped>
.visits-list {
  margin-top: 48px;
}

h2 {
  margin: 0 0 24px 0;
  font-size: 24px;
  font-weight: 600;
  color: #111827;
}

.loading, .no-visits {
  text-align: center;
  padding: 40px;
  color: #6b7280;
  font-size: 14px;
}

.visits-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.visit-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s;
}

.visit-item:hover {
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}

.visit-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: #eff6ff;
  border-radius: 50%;
  color: #3b82f6;
  flex-shrink: 0;
}

.visit-info {
  flex: 1;
  min-width: 0;
}

.visit-email {
  font-size: 15px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 4px;
}

.visit-details {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  font-size: 13px;
  color: #6b7280;
}

.visit-time {
  display: flex;
  align-items: center;
  gap: 4px;
}

.visit-token {
  font-family: monospace;
  font-size: 12px;
}
</style>
