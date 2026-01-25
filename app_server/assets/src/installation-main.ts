import { createApp } from 'vue';
import { createPinia } from 'pinia';

import AppInstallation from './AppInstallation.vue';
import './assets/styles.scss';
import './assets/installation.scss';

const app = createApp(AppInstallation);

app.use(createPinia());
app.mount('#app');
