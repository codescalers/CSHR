<template>
  <VToolbar color="primary">
    <VSpacer />
    <VMenu>
      <template #activator="{ props }">
        <VBtn icon="mdi-bell-outline" v-bind="props" />
      </template>

      <VList max-width="600" min-width="100%">
        <VListItem class="text-center" v-if="notifications.isLoading.value">
          <VProgressCircular indeterminate />
        </VListItem>
        <VListItem class="text-center" v-else-if="notifications.state.value.length === 0">
          You don't have any notification.
        </VListItem>
        <template v-else>
          <template
            v-for="(notification, index) in notifications.state.value"
            :key="notification.event_id"
          >
            <VListItem class="pa-4" @click="selectedNotificationIndex = index">
              <VListItemTitle class="text-wrap">
                {{ notification.title }}
              </VListItemTitle>

              <VListItemSubtitle>
                {{ notification.created_at }}
              </VListItemSubtitle>

              <template #append>
                <VChip
                  :color="getStatusColor(notification.type)"
                  :text="notification.type"
                  class="ml-4"
                />
              </template>
            </VListItem>

            <VDivider v-if="notifications.state.value.length > index + 1" />
          </template>
        </template>
      </VList>
    </VMenu>
    <VMenu>
      <template #activator="{ props }">
        <div class="d-flex justify-center align-center mx-2">
          <VProgressCircular indeterminate v-if="user.isLoading.value" />
          <VAvatar
            v-else-if="user.state.value"
            v-ripple
            v-bind="props"
            color="primary"
            class="border"
            :style="{ cursor: 'pointer' }"
          >
            <span class="text-h5 text-uppercase" v-text="user.state.value?.full_name[0] ?? '?'" />
          </VAvatar>
        </div>
      </template>

      <VList>
        <VListItem prepend-icon="mdi-account" title="Your Profile" to="/profile" />
        <VListItem
          prepend-icon="mdi-logout"
          title="Logout"
          class="text-error"
          @click="$emit('logout')"
        />
      </VList>
    </VMenu>

    <VDialog
      route-query="notification"
      :model-value="!!notification"
      @update:model-value="selectedNotificationIndex = undefined"
      min-width="min(94%, 1000px)"
    >
      <VCard>{{ notification }}</VCard>
    </VDialog>
  </VToolbar>
</template>

<script lang="ts">
import { computed } from 'vue'
import { useAsyncState } from '@vueuse/core'
import { useRouteQuery } from '@vueuse/router'
import { useApi } from '@/hooks'
import { getStatusColor } from '@/utils'

export default {
  name: 'CshrToolbar',
  setup() {
    const $api = useApi()
    const user = useAsyncState(() => $api.myprofile.getUser(), null)
    const notifications = useAsyncState(() => $api.notifications.list(), [])

    const selectedNotificationIndex = useRouteQuery<undefined | number>(
      'selected-notification',
      undefined,
      { transform: Number }
    )

    const notification = computed(() => {
      return notifications.state.value[selectedNotificationIndex.value ?? -1]
    })

    return { user, notifications, selectedNotificationIndex, notification, getStatusColor }
  }
}
</script>
