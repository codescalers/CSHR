<template>
  <VApp>
    <SideDrawer />
    <!-- <VNavigationDrawer expand-on-hover rail></VNavigationDrawer> -->
  </VApp>
</template>

<script lang="ts">
import { onMounted } from 'vue'

import { useApi } from '@/hooks'
import SideDrawer from '@/components/SideDrawer.vue'

export default {
  name: 'App',
  components: { SideDrawer },
  setup() {
    const api = useApi()
  }
}
</script>
