<template>
  <VDialog
    route-query="notification-dialog"
    :model-value="!!notification"
    @update:model-value="closeDialog"
    min-width="min(94%, 1000px)"
  >
    <NotificationDetails
      v-if="notification"
      :title="
        notification.type === 'vacations'
          ? capitalize(notification.reason.split('_').join(' '))
          : 'Applying for an HR Letter'
      "
      :eventId="notification.event_id"
      :sections="getSections(notification)"
      :status="notification.status"
      @close="closeDialog"
    />
  </VDialog>
</template>

<script lang="ts">
import { useRouteQuery } from '@vueuse/router'
import { watch, type PropType, capitalize } from 'vue'
import type { Api } from '@/types'
import { computedAsync } from '@vueuse/core'
import { useApi } from '@/hooks'

import NotificationDetails from './NotificationDetails.vue'

export default {
  name: 'NotificationDetailsDialog',
  components: { NotificationDetails },
  props: {
    modelValue: Object as PropType<Api.Returns.Notification>
  },
  emits: {
    'update:model-value': (value?: Api.Returns.Notification) => true || value
  },
  setup(props, ctx) {
    const $api = useApi()
    const selected = useRouteQuery<undefined | string>('selected-notification', undefined)
    const notification = computedAsync<any>(() => {
      const [type, id] = selected.value?.split('|') ?? []
      if (!isNaN(+id) && ['hr_letters', 'vacations'].includes(type)) {
        return $api.notifications.read(type, +id)
      }
      return undefined
    }, undefined)

    watch(
      () => props.modelValue,
      (notification) => {
        selected.value = notification ? `${notification.type}|${notification.event_id}` : undefined
      }
    )

    function getSections(data: any) {
      if (data.type === 'vacations')
        return [
          {
            title: 'Request Details',
            details: [
              { label: 'From Date', value: data.from_date },
              { label: 'End Date', value: data.end_date }
            ]
          },
          {
            title: 'Applying User',
            details: [
              { label: 'Name', value: data.applying_user.full_name },
              { label: 'Email', value: data.applying_user.email }
            ]
          },
          {
            title: 'Approval User',
            details: [
              { label: 'Name', value: data.approval_user.full_name },
              { label: 'Email', value: data.approval_user.email }
            ]
          }
        ]

      return [
        {
          title: 'User Details',
          details: [
            { label: 'Name', value: data.applying_user.full_name },
            { label: 'Email', value: data.applying_user.email },
            {
              label: 'Job Title',
              value: data.applying_user.job_title || 'Not specified'
            }
          ]
        },
        {
          title: 'Event Details',
          details: [
            { label: 'Status', value: data.status },
            { label: 'Approval User', value: data.approval_user || '-' },
            { label: 'With Date', value: data.with_date },
            { label: 'From Date', value: data.from_date },
            { label: 'End Date', value: data.end_date },
            { label: 'Salary Mentioned', value: data.with_salary_mentioned },
            { label: 'Addresses', value: data.addresses }
          ]
        }
      ]
    }

    function closeDialog() {
      selected.value = undefined
      ctx.emit('update:model-value')
    }

    return { selected, notification, closeDialog, getSections, capitalize }
  }
}
</script>
