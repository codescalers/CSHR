<template>
  <v-row class="d-flex justify-end">
    <div v-if="couldApprove && vacationStatus == 'pending'">
      <v-btn color="primary" class="ma-1" @click="handleApprove">Approve</v-btn>
      <v-btn color="error" class="ma-1" @click="handleReject">Reject</v-btn>
      <v-btn v-if="displayCloseBtn" color="info" class="ma-1" variant="flat" @click="$emit('update:closeDialog')">Close</v-btn>
      <v-spacer></v-spacer>
    </div>
    <div v-if="couldApprove && vacationStatus == 'requested_to_cancel'">
      <v-btn color="primary" class="ma-1" @click="handleCancelApprove">Approve the cancel request</v-btn>
      <v-btn color="error" class="ma-1" @click="handleCancelReject">Reject the cancel request</v-btn>
      <v-spacer></v-spacer>
    </div>
  </v-row>
</template>

<script lang="ts">
import { computed, ref, type PropType } from 'vue'
import type { Api, notificationType } from '@/types'
import { ApiClientBase } from '@/clients/api/base'
import { useAsyncState } from '@vueuse/core'
import { $api } from '@/clients'

export default {
  name: 'NotificationDetails',
  emits: ["update:vacation", "update:closeDialog"],
  props: {
    vacation: {
      type: Object as PropType<notificationType["request"]>,
      required: false
    },
    displayCloseBtn: {
      type: Boolean,
      required: false
    }
  },
  setup(props, { emit }) {
    const user = ApiClientBase.user
    const vacationStatus = ref(props.vacation!.status)


    async function handleApprove() {
      return useAsyncState($api.vacations.approve.update(props.vacation!.id), [] as unknown as Api.Vacation, {
        onSuccess(res: Api.Vacation) {
          vacationStatus.value = res.status
          emit("update:vacation", res)
          window.connections.ws.value!.send(
            JSON.stringify({
              event: 'approve_request',
              request_id: props.vacation!.id
            })
          )
        }
      })
    }

    async function handleReject() {
      return useAsyncState($api.vacations.reject.update(props.vacation!.id), [] as unknown as Api.Vacation, {
        onSuccess(res: Api.Vacation) {
          vacationStatus.value = res.status
          emit("update:vacation", res)
          window.connections.ws.value!.send(
            JSON.stringify({
              event: 'reject_request',
              request_id: props.vacation!.id
            })
          )
        }
      })
    }

    async function handleCancelApprove(){
      return useAsyncState($api.vacations.approve.cancel(props.vacation!.id), [] as unknown as Api.Vacation, {
        onSuccess(res: Api.Vacation) {
          vacationStatus.value = res.status
          emit("update:vacation", res)
          window.connections.ws.value!.send(
            JSON.stringify({
              event: 'approve_cancel_request',
              request_id: props.vacation!.id
            })
          )
        }
      })
    }

    async function handleCancelReject(){
      return useAsyncState($api.vacations.reject.cancel(props.vacation!.id), [] as unknown as Api.Vacation, {
        onSuccess(res: Api.Vacation) {
          vacationStatus.value = res.status
          emit("update:vacation", res)
          window.connections.ws.value!.send(
            JSON.stringify({
              event: 'reject_cancel_request',
              request_id: props.vacation!.id
            })
          )
        }
      })
    }

    const couldApprove = computed(() => {
      if( user.value?.id && props.vacation!.approvals.includes(user.value?.id)){
        return true
      }
      return false
    })

    return {
      couldApprove,
      vacationStatus,
      handleApprove,
      handleReject,
      handleCancelApprove,
      handleCancelReject,
    }
  }
}
</script>