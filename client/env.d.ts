/// <reference types="vite/client" />

interface ImportMetaEnv {
  VITE_DEBUG: 'true' | 'false'
  VITE_TITLE: string
  VITE_FAVICON: string
  VITE_LOGO: string
  SERVER_DOMAIN_NAME_API: string
  SERVER_DOMAIN_NAME_WS: string
}
