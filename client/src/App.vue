<template>
  <VApp>
    {{ Object.keys($globals || {}) }}
    {{ $metaEnv.VITE_LOGO }}
  </VApp>
</template>

<script lang="ts">
import { useGlobals } from '@/hooks'

export default {
  name: 'App',
  setup() {
    const globals = useGlobals()

    console.log(globals, globals.app)

    return { env: import.meta.env.VITE_CSHR_API }
  }
}
</script>
