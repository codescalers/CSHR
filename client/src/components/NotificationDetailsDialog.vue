<template>
  <VDialog route-query="notification" model-value min-width="min(94%, 1000px)">
    <!-- @update:model-value="selectedNotificationIndex = undefined" -->
    <VCard>{{ modelValue }}</VCard>
  </VDialog>
</template>

<script lang="ts">
import { useRouteQuery } from '@vueuse/router'
import { watch, type PropType } from 'vue'
import { watchThrottled } from '@vueuse/core'

export default {
  name: 'NotificationDetailsDialog',
  props: {
    modelValue: Object as PropType<Notification>
  },
  setup(props) {
    const type = useRouteQuery<undefined | string>('selected-type', undefined)
    const id = useRouteQuery<undefined | string>('selected-notification', undefined)

    watchDebounced(
      () => props.modelValue,
      (notification) => {},
      { debounce: 100 }
    )

    // watch(
    //   () => props.modelValue,
    //   (id) => {
    //     selected.value = undefined
    //     selected.value = id
    //   }
    // )
  }
}
</script>
