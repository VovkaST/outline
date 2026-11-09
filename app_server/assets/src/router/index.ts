import { createRouter, createWebHistory, type RouteLocationNormalized } from 'vue-router';

import { buildCheckoutPath, buildCheckoutSuccessPath, deprecatedCheckoutSource } from '@/utils/checkoutUrl';

function legacyTaskRedirect(to: RouteLocationNormalized, success: boolean) {
  const source = deprecatedCheckoutSource();
  // Кода нет в карте — старая страница открывается как раньше, без редиректа.
  if (!source) return true;
  const taskId = String(to.params.taskId);
  const path = success ? buildCheckoutSuccessPath(source, taskId) : buildCheckoutPath(source, taskId);
  return { path, query: to.query };
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      // Перенаправление со старого URL на новый
      path: '/payment/app/tariffs/',
      redirect: (to) => {
        const { task, ...restQuery } = to.query;
        if (!task) return '/task/';
        const taskId = String(task);
        const source = deprecatedCheckoutSource();
        if (!source) return { path: `/task/${taskId}/`, query: restQuery };
        return { path: buildCheckoutPath(source, taskId), query: restQuery };
      },
    },
    {
      path: '/c/:source([A-Za-z0-9_-]+)/:taskId([\\d\\w-]+)/success/',
      name: 'payment-success',
      component: () => import('@/views/PaymentSuccessView.vue'),
      props: true,
    },
    {
      path: '/c/:source([A-Za-z0-9_-]+)/:taskId([\\d\\w-]+)/',
      name: 'app-tariffs',
      component: () => import('@/views/AppTariffSelectView.vue'),
      props: true,
    },
    {
      path: '/task/:taskId([\\d\\w-]+)/success/',
      component: () => import('@/views/PaymentSuccessView.vue'),
      props: true,
      beforeEnter: (to) => legacyTaskRedirect(to, true),
    },
    {
      path: '/task/:taskId([\\d\\w-]+)/',
      component: () => import('@/views/AppTariffSelectView.vue'),
      props: true,
      beforeEnter: (to) => legacyTaskRedirect(to, false),
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('@/views/NotFoundView.vue'),
    },
  ],
});

export default router;
