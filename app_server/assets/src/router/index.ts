import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      // Перенаправление со старого URL на новый
      path: '/payment/app/tariffs/',
      redirect: (to) => {
        const { task, ...restQuery } = to.query;
        return task ? { path: `/task/${task}/`, query: restQuery } : '/task/';
      },
    },
    {
      path: '/task/:taskId(\\d+)/',
      name: 'app-tariffs',
      component: () => import('@/views/AppTariffSelectView.vue'),
      props: true,
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('@/views/NotFoundView.vue'),
    },
  ],
});

export default router;
