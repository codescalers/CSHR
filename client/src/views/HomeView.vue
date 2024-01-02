<template>
  <VDialog route-query="home_dialog" v-model="openHomeDialog" fullscreen>
    <VCard>
      <VCardText>a</VCardText>
    </VCard>
  </VDialog>

  <button @click="openHomeDialog = !openHomeDialog">Open Dialog</button>
</template>

<script lang="ts">
import { ref } from 'vue'

export default {
  setup() {
    const openHomeDialog = ref(false)

    return { openHomeDialog }
  }
}
</script>
