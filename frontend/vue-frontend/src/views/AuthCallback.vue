<template>
  <div class="loading">
    <h2>Autenticando...</h2>
    <p>Por favor espera un momento.</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

onMounted(() => {
  // 1. Obtener el token de la URL
  const token = route.query.token;

  if (token) {
    // 2. Guardarlo en el navegador
    localStorage.setItem('token', token);
    console.log("Token guardado con éxito");
    
    // 3. Redirigir al Dashboard
    router.push('/dashboard');
  } else {
    // Si no hay token, algo salió mal
    console.error("No se recibió token");
    router.push('/');
  }
});
</script>

<style scoped>
.loading {
  text-align: center;
  margin-top: 50px;
}
</style>