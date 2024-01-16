<template>
  <calenderCshr />
</template>

<script lang="ts">
import calenderCshr from "@/components/calender.vue"
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
