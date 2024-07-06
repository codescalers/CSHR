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

    <NotificationDetails
      v-else-if="selected && notification.state.value"
      :modelValue.="$props.modelValue"
      :sections="getSections(notification.state.value)"
      :vacation="
        notification.state.value.request.type === 'vacations' ? notification.state.value.request : undefined
      "
      @close="closeDialog"
      @update:approve="handleApprove"
      @update:reject="handleReject"
      @update:approval-user="handleApprovalUser"
    />
  </VDialog>
</template>

<script lang="ts">
import { useRouteQuery } from '@vueuse/router'
import { watch, type PropType, capitalize, ref } from 'vue'
import type { Api, notificationType } from '@/types'
import { useAsyncState } from '@vueuse/core'
import { useApi } from '@/hooks'

import NotificationDetails from './NotificationDetails.vue'

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
    'update:approve': (value: string) => value,
    'update:reject': (value: string) => value
  },

  setup(props, ctx) {
    const $api = useApi()
    const applyingUser = ref<Api.User | null>()
    const approvalUser = ref<Api.User | null>()
    const selected = useRouteQuery<undefined | string>('selected-' + props.routeQuery, undefined)

    const notification = useAsyncState(
      async (selected?: string) => {
        const [type, id] = selected?.split('|') ?? []
        if (!isNaN(+id) && ['hr_letters', 'vacations'].includes(type)) {
          const response = await $api.notifications.getNotification(+props.modelValue.id)
          applyingUser.value = response.request.applying_user
          approvalUser.value = response.request.approval_user
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
          ? `${notification.request.type}|${notification.request.id}`
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
      if (data.request.type === 'vacations')
        return [
          {
            title: 'Request Details',
            details: [
              {
                label: 'From Date',
                value: `${new Date(data.request.from_date).toDateString()}`
              },
              { label: 'End Date', value: `${new Date(data.request.end_date).toDateString()}` }
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
            { label: 'Status', value: data.request.status },
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

    function handleApprove(value: string) {
      return ctx.emit('update:approve', value)
    }

    function handleReject(value: string) {
      return ctx.emit('update:reject', value)
    }

    function handleApprovalUser(user: Api.User) {
      approvalUser.value = user
    }

    return {
      selected,
      notification,
      closeDialog,
      getSections,
      capitalize,
      handleApprove,
      handleReject,
      handleApprovalUser
    }
  }
}
</script>
