<template>
  <calenderCshr />
</template>

<script lang="ts">
import { $api } from "@/clients";
import calenderCshr from "@/components/calender.vue"
import type { Api } from "@/types";
import { onMounted, ref } from "vue";
export default {
  name: 'CalendarView',
  components: {
    calenderCshr,
  },
  setup() {
    return {
      calenderCshr,
    }
  }
}
</script>
