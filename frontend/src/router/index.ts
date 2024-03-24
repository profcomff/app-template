import { RouteRecordRaw, createRouter, createWebHistory } from 'vue-router';

const routes: RouteRecordRaw[] = [
	{
		path: '/',
		redirect: '/main',
	},
	{
		path: '/main',
		component: () => import('../pages/MainPage.vue'),
	},
];

export const router = createRouter({
	history: createWebHistory(),
	routes,
});
