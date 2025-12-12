<template>
  <div class="visit-user-form">
    <h3>Visitar mapa de otro usuario</h3>
    
    <div class="form-group">
      <label for="email-input">Email del usuario:</label>
      <input
        id="email-input"
        v-model="emailToVisit"
        type="email"
        placeholder="usuario@ejemplo.com"
        class="input-field"
        @keyup.enter="visitUser"
      />
    </div>

    <button @click="visitUser" class="btn-visit" :disabled="loading || !emailToVisit">
      {{ loading ? 'Buscando...' : 'Ver mapa' }}
    </button>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const emailToVisit = ref('');
const loading = ref(false);
const error = ref('');

async function visitUser() {
  if (!emailToVisit.value) return;

  // Validar formato de email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(emailToVisit.value)) {
    error.value = 'Por favor ingresa un email válido';
    return;
  }

  loading.value = true;
  error.value = '';

  try {
    // Navegar a la vista de visita
    router.push({
      name: 'VisitMap',
      params: { email: emailToVisit.value }
    });
  } catch (err) {
    error.value = 'Error al buscar usuario';
    console.error(err);
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.visit-user-form {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-top: 24px;
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

.btn-visit {
  width: 100%;
  padding: 12px;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}

.btn-visit:hover:not(:disabled) {
  background: #059669;
}

.btn-visit:disabled {
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
