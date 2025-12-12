import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // Importamos el router

createApp(App)
  .use(router) // Usamos el router
  .mount('#app');
