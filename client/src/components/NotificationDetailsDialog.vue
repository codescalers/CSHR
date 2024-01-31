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
      :title="
        notification.state.value.type === 'vacations'
          ? capitalize(notification.state.value.reason.split('_').join(' '))
          : 'Applying for an HR Letter'
      "
      :eventId="notification.state.value.event_id"
      :sections="getSections(notification.state.value)"
      :status="notification.state.value.status"
      @close="closeDialog"
    />
  </VDialog>
</template>

<script lang="ts">
import { useRouteQuery } from '@vueuse/router'
import { watch, type PropType, capitalize } from 'vue'
import type { Api } from '@/types'
import { useAsyncState } from '@vueuse/core'
import { useApi } from '@/hooks'

import NotificationDetails from './NotificationDetails.vue'

export default {
  name: 'NotificationDetailsDialog',
  components: { NotificationDetails },
  props: {
    routeQuery: { type: String, required: true },
    modelValue: Object as PropType<Api.Returns.Notification>
  },
  emits: {
    'update:model-value': (value?: Api.Returns.Notification) => true || value
  },
  setup(props, ctx) {
    const $api = useApi()
    const selected = useRouteQuery<undefined | string>('selected-' + props.routeQuery, undefined)
    const notification = useAsyncState(
      async (selected?: string) => {
        const [type, id] = selected?.split('|') ?? []
        if (!isNaN(+id) && ['hr_letters', 'vacations'].includes(type)) {
          return $api.notifications.read(type, +id)
        }
        return undefined
      },
      undefined,
      { immediate: false }
    )

    watch(
      () => props.modelValue,
      (notification) => {
        selected.value = notification ? `${notification.type}|${notification.event_id}` : undefined
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
