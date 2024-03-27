<template>
  <VAlert
    :type="notification.type === 'default' ? undefined : notification.type"
    :closable="notification.closable"
    @click:close="notification.destroy()"
    @mouseenter="
      notification.persistent || !notification.pauseOnHover
        ? undefined
        : destroyTimer.pauseTimeout()
    "
    @mouseleave="
      notification.persistent || !notification.pauseOnHover
        ? undefined
        : destroyTimer.resumeTimeout()
    "
  >
    <template #title>
      <span v-if="notification.title" v-html="notification.title" />
    </template>

    <template #text>
      <span v-if="notification.description" v-html="notification.description" />
    </template>
  </VAlert>
</template>

<script lang="ts">
import { makeNotifierProps, useDestroyTimer } from 'vue3-notifier'

export default {
  name: 'CustomNotification',
  props: makeNotifierProps(),
  setup(props) {
    const destroyTimer = useDestroyTimer(
      props.notification,
      props.pluginOptions,
      props.notification.destroy
    )

    return { destroyTimer }
  }
}
</script>
