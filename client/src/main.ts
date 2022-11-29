import App from './App.svelte';

const app = new App({
  target: document.body,
  props: {
    name: 'world'
  }
});

interface AppConfigs {
  SERVER_API_URL: string;
  APP_BASE_API_URL: string;
};

declare global {
  interface Window {
    configs: AppConfigs;
  }
};

export default app;