<template>
  <VDialog
    :route-query="routeQuery + '-dialog'"
    :model-value="!!selected"
    @update:model-value="closeDialog"
    min-width="min(94%, 1000px)"
  >
    <div class="d-flex justify-center align-center" v-if="notification.isLoading.value && selected">
      <VCard>
        <VCardText>
          <VProgressCircular indeterminate />
        </VCardText>
      </VCard>
    </div>
    <template v-else-if="selected && notification.state.value">
      <NotificationDetails
      v-if="couldAccessNotification"
      :modelValue.="$props.modelValue"
      :sections="getSections(notification.state.value)"
      :request-status="requestStatus"
      :vacation="
          notification.state.value.request.type === 'vacation' ? notification.state.value.request : undefined
        "
        @close="closeDialog"
        @update:vacation="updateVacation($event)"
      />
      <div v-else class="not-allowed">
        <v-container>
          <v-toolbar type="warning" class="pl-5" height="40">
            <v-icon class="mr-2 d-flex align-center" color="warning">mdi-alert</v-icon>
            <p class="d-flex align-center" style="font-size: 18px;">Admin Area</p>
          </v-toolbar>
          <v-card class="pa-3">
            <v-card-text>
              <strong>You are not allowed to access this content.</strong>
            </v-card-text>
          </v-card>
        </v-container>
      </div>
    </template>
  </VDialog>
</template>

<script lang="ts">
import { useRouteQuery } from '@vueuse/router'
import { watch, type PropType, capitalize, ref, computed } from 'vue'
import type { Api, notificationType } from '@/types'
import { useAsyncState } from '@vueuse/core'
import { useApi } from '@/hooks'

import NotificationDetails from './NotificationDetails.vue'
import { useNotificationStore } from '@/stores/notifications'

export default {
  name: 'NotificationDetailsDialog',
  components: { NotificationDetails },
  props: {
    routeQuery: { type: String, required: true },
    modelValue: {
      type: Object as PropType<notificationType>,
      required: true
    }
  },
  emits: {
    'update:model-value': (value?: notificationType) => true || value,
    'set:notification': (value: notificationType) => value
  },

  setup(props, ctx) {
    const $api = useApi()
    const applyingUser = ref<Api.User | null>()
    const approvalUser = ref<Api.User | null>()
    const requestStatus = ref<Api.RequestStatus>()
    const selected = useRouteQuery<undefined | string>('selected-' + props.routeQuery, undefined)
    const notificationsStore = useNotificationStore()
    const notifications = computed(() => notificationsStore.notifications)
    const couldAccessNotification = computed(() => {
      return notifications.value.filter(_notification => _notification.id === notification.state.value?.id).length
    })

    const notification = useAsyncState(
      async (selected?: string) => {
        const [type, id] = selected?.split('|') ?? []
        if (!isNaN(+id) && ['hr_letters', 'vacation'].includes(type)) {
          const response = await $api.notifications.getNotification(+id)
          applyingUser.value = response.request.applying_user
          approvalUser.value = response.request.approval_user
          requestStatus.value = response.request.status
          ctx.emit("set:notification", response)
          return response
        }
        return undefined
      },
      undefined,
      {
        immediate: false,
        onError: (error) => {
          console.error('Error fetching notification:', error)
          closeDialog()
        }
      }
    )

    watch(
      () => props.modelValue,
      (notification) => {
        selected.value = notification
          ? `${notification.request.type}|${notification.id}`
          : undefined
      }
    )

    watch(
      selected,
      (value) => {
        notification.execute(undefined, value)
      },
      { immediate: true }
    )

    function getSections(data: any) {
      if (data.request.type === 'vacation')
        return [
          {
            title: 'Request Details',
            details: [
              {
                label: 'From Date',
                value: `${new Date(data.request.from_date).toDateString()}`
              },
              { label: 'End Date', value: `${new Date(data.request.end_date).toDateString()}` },
            ]
          },
          {
            title: 'Applying User',
            details: [
              { label: 'Name', value: applyingUser.value ? applyingUser.value.full_name : "Not specified" },
              { label: 'Email', value: applyingUser.value ? applyingUser.value.email : "Not specified" }
            ]
          },
          {
            title: 'Approval User',
            details: [
              { label: 'Name', value: approvalUser.value ? approvalUser.value.full_name : 'Not specified' },
              { label: 'Email', value: approvalUser.value ? approvalUser.value.email : 'Not specified' }
            ]
          }
        ]

      return [
        {
          title: 'User Details',
          details: [
            { label: 'Name', value: applyingUser.value ? applyingUser.value.full_name : "Not specified" },
            { label: 'Email', value: applyingUser.value ? applyingUser.value.email : "Not specified" },
            {
              label: 'Job Title',
              value: applyingUser.value ? applyingUser.value.job_title : 'Not specified'
            }
          ]
        },
        {
          // TODO: Enable the HR letter and the official docs
          title: 'Event Details',
          details: [
            { label: 'Approval User', value: approvalUser.value ? approvalUser.value.full_name : 'Not specified' },
            // { label: 'With Date', value: data.with_date },
            // { label: 'From Date', value: data.from_date },
            // { label: 'End Date', value: data.end_date },
            // { label: 'Salary Mentioned', value: data.with_salary_mentioned },
            // { label: 'Addresses', value: data.addresses }
          ]
        }
      ]
    }

    function closeDialog() {
      selected.value = undefined
      ctx.emit('update:model-value')
    }

    function updateVacation(vacation: Api.Vacation) {
      requestStatus.value = vacation.status;
      applyingUser.value = vacation.applying_user;
      approvalUser.value = vacation.approval_user;
    }

    return {
      selected,
      notification,
      closeDialog,
      getSections,
      capitalize,
      requestStatus,
      updateVacation,
      couldAccessNotification,
    }
  }
}
</script>

<style>
.not-allowed{
  width: 550px !important;
  margin: 0 auto;
}
</style>
