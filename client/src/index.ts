export {};

declare global {
  interface Window {
    env: {
      CSHR_API: string;
    };
  }
}
