<template>
  <v-card class="pa-4">
    <div class="my-2">
      <v-row class="mb-0">
        <v-col class="d-flex justify-start mb-0">
          <v-card-title class="font-weight-bold mb-0"> {{ $props.modelValue.title }} </v-card-title>
        </v-col>
        <v-col class="d-flex justify-end pb-0">
          <v-card-subtitle>
            <v-chip :color="getStatusColor(vacationStatus)">
              {{ vacationStatus }}
            </v-chip>
          </v-card-subtitle>
        </v-col>
      </v-row>
      <v-card-text class="mt-0 pt-0">
        <p>
          {{ $props.modelValue.body }}
        </p>
      </v-card-text>
    </div>
    
    <v-row no-gutters class="mx-3">
      <v-col v-for="section in sections" :key="section.key" cols="12">
        <v-card class="mb-6 elevation-12">
          <v-card-title class="card-title bg-primary white--text">{{ section.title }}</v-card-title>

          <v-list class="custom-list">
            <v-row
              v-for="detail in section.details"
              :key="detail.label"
              class="ma-1 bordered"
              no-gutters
            >
              <v-col cols="3">
                <v-list-item>
                  <v-list-item-content class="ma-0">
                    {{ detail.label }}
                  </v-list-item-content>
                </v-list-item>
              </v-col>

              <v-col cols="9">
                <v-list-item>
                  <v-list-item-content>
                    {{ detail.value }}
                  </v-list-item-content>
                </v-list-item>
              </v-col>
            </v-row>
          </v-list>
        </v-card>
      </v-col>
    </v-row>

    <v-card-actions class="d-flex justify-end">
      <v-row class="d-flex justify-end mt-3">
        <div v-if="couldApprove && vacationStatus == 'pending'">
          <v-btn variant="tonal" color="primary" class="ma-1" @click="handleApprove">Approve</v-btn>
          <v-btn variant="tonal" color="error" class="ma-1" @click="handleReject">Reject</v-btn>
          <v-spacer></v-spacer>
        </div>
        <v-btn color="info" class="ma-1" variant="flat" @click="closeDialog()">Close</v-btn>
      </v-row>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { computed, ref, type PropType } from 'vue'
import { getStatusColor } from '@/utils'
import type { Api, notificationType } from '@/types'
import { ApiClientBase } from '@/clients/api/base'
import { useAsyncState } from '@vueuse/core'
import { $api } from '@/clients'

export default {
  name: 'NotificationDetails',
  emits: ["update:approve", "update:reject", "update:approvalUser"],
  props: {
    modelValue: {
      type: Object as PropType<notificationType>,
      required: true
    },
    sections: {
      type: Array as PropType<any[]>,
      required: true
    },
    vacation: {
      type: Object as PropType<Api.Vacation>,
      required: true
    },
    onClose: {
      type: Function as PropType<() => void>,
      required: true
    }
  },
  setup(props, { emit }) {
    const color = computed(() => getStatusColor(props.modelValue.request.status))
    const user = ApiClientBase.user
    const vacationStatus = ref(props.modelValue.request.status)

    const closeDialog = () => {
      props.onClose()
    }

    async function handleApprove() {
      return useAsyncState($api.vacations.approve.update(props.vacation.id), [], {
        onSuccess() {
          vacationStatus.value = 'approved'
          emit("update:approve", vacationStatus.value)
          emit("update:approvalUser", user.value)
        }
      })
    }

    async function handleReject() {
      return useAsyncState($api.vacations.reject.update(props.vacation.id), [], {
        onSuccess() {
          vacationStatus.value = 'rejected'
          emit("update:reject", vacationStatus.value)
          emit("update:approvalUser", user.value)
        }
      })
    }

    const couldApprove = computed(() => {
      if( user.value?.id && props.modelValue.receivers.includes(user.value?.id)){
        return true
      }
      return false
    })

    return {
      color,
      couldApprove,
      vacationStatus,
      closeDialog,
      getStatusColor,
      handleApprove,
      handleReject
    }
  }
}
</script>

<style scoped>
.card-title {
  font-size: 1rem !important;
  line-height: 1.5rem !important;
}
</style>
