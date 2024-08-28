<template>
  <VToolbar color="primary">
    <VSpacer />
    <VMenu v-model="menu">
      <template #activator="{ props }">
        <VBtn
          icon="mdi-bell-badge-outline"
          size="large"
          v-bind="props"
          color="white"
          v-if="hasReadNotifications"
        />
        <VBtn icon="mdi-bell-outline" size="large" v-bind="props" color="white" v-else />
      </template>

      <VList
        max-width="600"
        min-width="100%"
        :height="notifications.length ? 700 : 'auto'"
        class="mt-1"
      >
        <v-toolbar color="#262b2e" class="mb-2">
          <v-btn
            :disabled="!notifications.length || !hasReadNotifications || isLoadingReadDeleteAll"
            type="info"
            color="success"
            variant="tonal"
            class="mr-2"
            :loading="isLoadingReadDeleteAll"
            @click="handleReadAllNotifications"
          >
            <v-icon>mdi-read</v-icon>
            Mark all as read
          </v-btn>
          <v-btn
            :disabled="!notifications.length || isLoadingReadDeleteAll"
            type="info"
            color="error"
            variant="outlined"
            :loading="isLoadingReadDeleteAll"
            @click="handleDeleteAllNotifications"
          >
            <v-icon>mdi-trash-can</v-icon>
            Delete all notifications
          </v-btn>
        </v-toolbar>

        <VListItem class="text-center" v-if="isLoading">
          <VProgressCircular indeterminate />
        </VListItem>
        <VListItem class="text-center" v-else-if="notifications.length === 0">
          You don't have any notification.
        </VListItem>
        <template v-else>
          <template v-for="(notification, index) in notifications" :key="notification.id">
            <VListItem
              class="pa-4 mt-1 mb-1"
              @click="setNotification(notification)"
              :style="{ background: !notification.is_read ? 'rgb(37 58 86 / 43%)' : 'transparent' }"
            >
              <VListItemTitle class="text-wrap">
                <span class="is-not-read" v-if="!notification.is_read"></span>
                {{ notification.title }}
              </VListItemTitle>

              <VListItemSubtitle>
                ( {{ formatedDate(notification.created_at) }} )
              </VListItemSubtitle>
            </VListItem>

            <VDivider v-if="notifications.length > index + 1" />
          </template>
        </template>
      </VList>
    </VMenu>

    <VMenu>
      <template #activator="{ props }">
        <div class="d-flex justify-center align-center mx-2">
          <VProgressCircular indeterminate v-if="isUserLoading" />
          <profileImage
            width="55px"
            v-else-if="user"
            :with-link="false"
            :user="user"
            v-bind="props"
          />
        </div>
      </template>

      <VList class="mt-1">
        <VListItem
          prepend-icon="mdi-account"
          title="Your Profile"
          @click="$router.push('/profile')"
        />
        <VListItem
          prepend-icon="mdi-logout"
          title="Logout"
          class="text-error"
          @click="$emit('logout')"
        />
      </VList>
    </VMenu>

    <NotificationDetailsDialog
      route-query="toolbar-notification"
      v-model="selectedNotification"
      @set:notification="setNotification"
    />
  </VToolbar>
</template>

<script lang="ts">
import { computed, onMounted, ref, type Ref } from 'vue'
import { useAsyncState } from '@vueuse/core'
import { useApi } from '@/hooks'
import { formatDate, getStatusColor } from '@/utils'
import type { notificationType } from '@/types'
import NotificationDetailsDialog from './NotificationDetailsDialog.vue'
import profileImage from './profileImage.vue'
import { useNotificationStore } from '@/stores/notifications'
import { ApiClientBase } from '@/clients/api/base'

export default {
  name: 'CshrToolbar',
  components: { NotificationDetailsDialog, profileImage },
  setup() {
    const $api = useApi()
    const user = useAsyncState(() => $api.myprofile.getUser(), null)
    const notificationStore = useNotificationStore()
    const menu = ref(false)
    const isLoading = ref(true)
    const isLoadingReadDeleteAll = ref(false)

    const notifications = computed(() => notificationStore.notifications)

    onMounted(async () => {
      await user.execute();
      if (!user.state.value) {
        window.location.href = '/login'
      }
    })

    const loadNotifications = async () => {
      const notificationData = await $api.notifications.list()
      notificationStore.setNotifications(notificationData)
      isLoading.value = false
    }

    loadNotifications()

    function formatedDate(date: string) {
      const _date = new Date(date)
      const _formatDate = formatDate(date)
      const time = _date.toLocaleTimeString()
      return `${_formatDate} - ${time}`
    }

    const selectedNotification = ref<notificationType>() as Ref<notificationType>


    const setNotification = async (notification: notificationType) => {
      selectedNotification.value = notification
      if (!selectedNotification.value.is_read) {
        selectedNotification.value.is_read = true
        await $api.notifications.readNotification(
          selectedNotification.value.id,
          selectedNotification.value.is_read
        )
      }
    }

    const hasReadNotifications = computed(() => {
      return notificationStore.notifications.some((notification) => !notification.is_read)
    })

    const handleReadAllNotifications = async (event: Event) => {
      event.preventDefault()
      event.stopPropagation()
      await readAllNotifications()
      menu.value = true
    }

    const handleDeleteAllNotifications = async (event: Event) => {
      event.preventDefault()
      event.stopPropagation()
      await deleteAllNotifications()
      menu.value = true
    }

    const readAllNotifications = async () => {
      isLoadingReadDeleteAll.value = true
      const me = ApiClientBase.user.value?.fullUser
      if (me) {
        const notifications = await $api.notifications.readAllNotifications(me.id)
        notificationStore.setNotifications(notifications)
      }
      isLoadingReadDeleteAll.value = false
    }

    const deleteAllNotifications = async () => {
      isLoadingReadDeleteAll.value = true
      const me = ApiClientBase.user.value?.fullUser
      if (me) {
        await $api.notifications.deleteAllNotifications(me.id)
        notificationStore.clearNotifications()
      }
      isLoadingReadDeleteAll.value = false
    }

    return {
      user: user.state,
      isUserLoading: user.isLoading,
      notifications,
      isLoading,
      isLoadingReadDeleteAll,
      selectedNotification,
      hasReadNotifications,
      getStatusColor,
      formatedDate,
      setNotification,
      handleReadAllNotifications,
      handleDeleteAllNotifications,
      menu
    }
  }
}
</script>

<style scoped>
.is-not-read {
  padding: 5px;
  content: '';
  display: inline-block;
  background-color: rgb(42, 165, 93);
  border-radius: 50%;
}
</style>
