import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import AuthCallback from '../views/AuthCallback.vue';
import Dashboard from '../views/Dashboard.vue';
import VisitMap from '../views/VisitMap.vue';

const routes = [
  { path: '/', component: Login },
  { path: '/auth-callback', component: AuthCallback },
  { 
    path: '/dashboard', 
    component: Dashboard,
    meta: { requiresAuth: true } // Marca personalizada
  },
  {
    path: '/visit/:email',
    name: 'VisitMap',
    component: VisitMap,
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Guardián de Navegación (Navigation Guard)
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');

  // Si la ruta requiere auth y no hay token -> Login
  if (to.meta.requiresAuth && !token) {
    next('/');
  } 
  // Si vas al login pero ya tienes token -> Dashboard
  else if (to.path === '/' && token) {
    next('/dashboard');
  } 
  else {
    next(); // Continuar normal
  }
});

export default router;