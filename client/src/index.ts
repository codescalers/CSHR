export {};

declare global {
  interface Window {
    env: {
      SERVER_DOMAIN_NAME_API: string;
      SERVER_DOMAIN_NAME_WS: string;
    };
  }
}
