import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/app/',
      name: 'app-main',
      children: [
        {
          path: 'tariffs/',
          name: 'app-tariffs',
          component: () => import('@/views/AppTariffSelectView.vue'),
        },
      ],
    },
  ],
});

export default router;
