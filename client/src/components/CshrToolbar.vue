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
            <VListItem class="pa-4" @click="selectedNotification = notification">
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
          <profileImage v-else-if="user.state.value" :with-link="false" :user="user.state.value" v-bind="props" />
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
    <NotificationDetailsDialog route-query="toolbar-notification" v-model="selectedNotification" />
  </VToolbar>
</template>

<script lang="ts">
import { ref } from 'vue'
import { useAsyncState } from '@vueuse/core'
import { useApi } from '@/hooks'
import { getStatusColor } from '@/utils'
import type { Api } from '@/types'
import NotificationDetailsDialog from './NotificationDetailsDialog.vue'
import profileImage from './profileImage.vue'

export default {
  name: 'CshrToolbar',
  components: { NotificationDetailsDialog, profileImage },
  setup() {
    const $api = useApi()
    const user = useAsyncState(() => $api.myprofile.getUser(), null)
    const notifications = useAsyncState(() => $api.notifications.list(), [])
    const selectedNotification = ref<Api.Returns.Notification>()

    return { user, notifications, selectedNotification, getStatusColor }
  }
}
</script>
