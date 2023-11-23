import App from "./App.svelte";

const app = new App({
  target: document.body,
});

interface AppConfigs {
  SERVER_BASE_URL: string;
  SERVER_API_URL: string;
}

declare global {
  interface Window {
    configs: AppConfigs;
  }
}

export default app;
