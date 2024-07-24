<template>
  <v-card elevation="0">
    <v-card-title class="bg-graytitle">
      <div class="d-flex flex-row-reverse">
        <v-icon class="me-2" size="small" @click.stop="$emit('close-dialog', false)">
          mdi-close
        </v-icon>
      </div>
    </v-card-title>
    <v-container class="pa-6">
      <p class="text-subtitle-1 text-center">
        From <b>{{ formatDateTime(startDate) }} </b> to <b>{{ formatDateTime(endDate) }} </b> vacation
      </p>

      <v-form ref="form" @submit.prevent="updateVacation()">
        <v-row class="d-flex justify-center my-2">
          <v-btn color="primary" v-if="couldUpdate && vacation.applying_user.id === user?.id" class="mx-1 my-2" type="submit"
            :disabled="!form?.isValid">Update</v-btn>
          <v-btn v-if="vacation.status === 'approved' && couldDelete" color="error" class="mx-1 my-2" @click="requestToCancel">Request to Cancel</v-btn>
          <v-btn v-if="vacation.status === 'pending' && couldDelete" color="error" class="mx-1 my-2" @click="handleDelete">Cancel</v-btn>
        </v-row>
        <div v-if="couldApprove && vacation.status == 'requested_to_cancel'">
          <v-divider class="my-2"></v-divider>
          <v-alert class="my-2" type="warning">
            {{ vacation.applying_user.full_name }} is requesting an action to cancel the vacation request.
          </v-alert>
        </div>
        <v-divider class="my-2"></v-divider>
        <v-card elevation="0" class="pa-4">
          <v-row class="py-2">
            <v-col cols="6" class="d-flex">
              <v-icon class="mr-2">mdi-account</v-icon>
              <p>
                Applying User :
                <span color="warning" class="mx-2">
                  {{ vacation.applying_user.full_name }}
                </span>
              </p>
            </v-col>
            <v-col cols="6" class="d-flex items-center">
              <p>
                Status :
                <span :style="{color: getStatusColor(vacation.status)}">{{ formatRequestStatus(vacation.status) }}</span>
              </p>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="6">
              <v-text-field color="info" item-color="info" base-color="info" variant="outlined" hide-details="auto"
                label="From" v-model="startDate" :readonly="!couldUpdate" type="datetime-local" :rules="[validateStartDate]" @input="validateForm">
              </v-text-field>
            </v-col>
            <v-col cols="6">
              <v-text-field color="info" item-color="info" base-color="info" variant="outlined" hide-details="auto"
                label="To" v-model="endDate" :readonly="!couldUpdate" type="datetime-local" :rules="[validateEndDate]" @input="validateForm">
              </v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="6">
              <v-autocomplete color="info" item-color="info" base-color="info" variant="outlined" v-model="leaveReason"
                :items="leaveReasons" label="Reason" return-object item-title="name" :readonly="!couldUpdate">
              </v-autocomplete>
            </v-col>
            <v-col cols="6">
              <v-text-field color="info" item-color="info" base-color="info" variant="outlined" hide-details="auto"
                label="Requested Days" v-model="actualDays" readonly>
              </v-text-field>
            </v-col>
          </v-row>

        </v-card>
      </v-form>
      <v-divider class="my-2"></v-divider>
      <!-- Approve/Reject the normal request -->
      <v-row class="d-flex justify-end mt-3" v-if="couldApprove && vacation.status == 'pending'">
        <v-btn color="primary" class="ma-1" type="submit"
        :disabled="!form?.isValid || disabled" @click="updateVacation" v-if="couldUpdate && vacation.applying_user.id !== user?.id && user?.fullUser.location.id == vacation.applying_user.location.id">Update</v-btn>
        <v-btn color="primary" class="ma-1" @click="handleApprove">Approve</v-btn>
        <v-btn color="error" class="ma-1" @click="handleReject">Reject</v-btn>
      </v-row>
      <!-- Approve/Reject the cancel request -->
      <v-row class="d-flex justify-end mt-3" v-if="couldApprove && vacation.status == 'requested_to_cancel'">
        <v-btn color="primary" class="ma-1" @click="handleCancelApprove">Approve the cancel request</v-btn>
        <v-btn color="error" class="ma-1" @click="handleCancelReject">Reject the cancel request</v-btn>
      </v-row>
    </v-container>
  </v-card>
</template>
<script lang="ts">
import type { Api } from '@/types';
import { capitalize, computed, onMounted, ref, watch } from 'vue';
import { calculateTimes, convertToTimeOnly, formatDateTime } from '@/utils'

import { useApi } from '@/hooks'
import { useAsyncState } from '@vueuse/core'
import { ApiClientBase } from '@/clients/api/base'
import type { PropType } from 'vue';
import { formatRequestStatus, getStatusColor } from '@/utils';

export default {
  name: 'vacationCard',
  props: {
    vacation: {
      type: Object as PropType<Api.Vacation>,
      required: true,
    }
  },
  emits: {
    'close-dialog': (item: Boolean) => item,
    'update-vacation': (item: any) => item,
    'cancel-vacation': () => true,
    'status-vacation': (item: Api.RequestStatus) => item
  },

  setup(props, ctx) {
    const $api = useApi()
    const startDate = ref<string>(props.vacation.from_date);
    const endDate = ref<string>(props.vacation.end_date);
    const actualDays = ref<number>(props.vacation.actual_days);

    const leaveReason = ref<Api.LeaveReason>({
      name: transformString(props.vacation.reason),
      reason: props.vacation.reason
    })
    const form = ref()
    const disabled = ref<boolean>(true)
    const user = ApiClientBase.user
    const leaveReasons = ref<Api.LeaveReason[]>([])
  
    async function validateForm() {
      await form.value.validate();
    }

    const couldUpdate = computed(() => {
      const currentUser = user.value?.fullUser;
      const vacationUser = props.vacation?.applying_user;
      if (user.value && props.vacation.status === 'pending') {
        return (
          (currentUser?.id === vacationUser.id) ||
          (currentUser?.user_type !== "User") && (currentUser && props.vacation.approvals.includes(currentUser.id))
        );
      }
      return false;
    });

    const balance = useAsyncState(
      () => $api.vacations.getVacationBalance({ user_ids: user.value?.fullUser.id }),
      null,
      {
        immediate: false,
        onSuccess(data: any) {
          leaveReasons.value = [
            {
              name: `Emergency Leaves  ${data[0].emergency_leaves.reserved} / ${data[0].emergency_leaves.all}`,
              reason: 'emergency_leaves'
            },
            {
              name: `Sick Leaves  ${data[0].sick_leaves.reserved} / ∞`,
              reason: 'sick_leaves'
            },
            {
              name: `Annual Leaves  ${data[0].annual_leaves.reserved} / ${data[0].annual_leaves.all}`,
              reason: 'annual_leaves'
            },
            {
              name: `Unpaid ${data[0].unpaid.reserved} / ∞`,
              reason: 'unpaid'
            },
            {
              name: `Compensation  ${data[0].compensation.reserved} / ∞`,
              reason: 'compensation'
            },
            {
              name: `Leave Excuse  ${data[0].leave_excuses.reserved} / ${data[0].leave_excuses.all}`,
              reason: 'leave_excuses'
            }
          ]
        }
      }
    )

    onMounted(() => {
      balance.execute();
    })

    const couldDelete = computed(() => {
      if (user.value) {
        // Could delete if user signed in is the same user applied for vacation
        if (props.vacation.applying_user.id == user.value.fullUser.id) {
          return true
        }
        // Could delete if applying user reports  admin logged in 
        // and works from the same office
        if (
          user.value.fullUser.user_type === "Admin" &&
          props.vacation.applying_user.location.name === user.value.fullUser.location.name
        ) {
          return true
        }
        return false
      }
      return false
    })

    const couldApprove = computed(() => {
      if (user.value?.id && props.vacation.approvals?.includes(user.value?.id)) {
        return true
      }
      return false
    })

    watch([leaveReason, startDate, endDate], ([newLeaveReason, newStartDate, newEndDate], [oldLeaveReason, oldStartDate, oldEndDate]) => {
      if (newLeaveReason.name !== oldLeaveReason.name || newStartDate !== oldStartDate || newEndDate !== oldEndDate) {
        disabled.value = false;
        return
      }
      disabled.value = true;
    });

    function validateStartDate(value: any) {
      const start = new Date(value);
      const end = new Date(endDate.value);

      if (start > end) {
        return 'From date must be before to date.'
      }
      return true
    }

    function validateEndDate(value: any) {
      const start = new Date(value);
      const end = new Date(endDate.value);
      if (end < start) {
        return 'To date must be after from date.'
      }
      return true
    }

    async function handleDelete() {
      return useAsyncState($api.vacations.cancel(props.vacation.id), [], {
        onSuccess() {
          ctx.emit('cancel-vacation')
          window.connections.ws.value!.send(
            JSON.stringify({
              event: 'cancel_request',
              request_id: props.vacation.id
            })
          )
        }
      })
    }

    async function requestToCancel() {
      return useAsyncState($api.vacations.requestToCancel(props.vacation.id), [] as unknown as Api.Vacation, {
        onSuccess(res: Api.Vacation) {
          ctx.emit('status-vacation', res.status)
          window.connections.ws.value!.send(
            JSON.stringify({
              event: 'request_to_cancel_request',
              request_id: props.vacation.id
            })
          )
        }
      })
    }

    async function handleApprove() {
      return useAsyncState($api.vacations.approve.update(props.vacation.id), [] as unknown as Api.Vacation, {
        onSuccess(res: Api.Vacation) {
          ctx.emit('status-vacation', res.status)
          window.connections.ws.value!.send(
            JSON.stringify({
              event: 'approve_request',
              request_id: props.vacation.id
            })
          )
        }
      })
    }

    async function handleReject() {
      return useAsyncState($api.vacations.reject.update(props.vacation.id), [] as unknown as Api.Vacation, {
        onSuccess(res: Api.Vacation) {
          ctx.emit('status-vacation', res.status)
          window.connections.ws.value!.send(
            JSON.stringify({
              event: 'reject_request',
              request_id: props.vacation.id
            })
          )
        }
      })
    }

    async function handleCancelApprove(){
      return useAsyncState($api.vacations.approve.cancel(props.vacation.id), [] as unknown as Api.Vacation, {
        onSuccess(res: Api.Vacation) {
          ctx.emit('status-vacation', res.status)
          window.connections.ws.value!.send(
            JSON.stringify({
              event: 'approve_cancel_request',
              request_id: props.vacation.id
            })
          )
        }
      })
    }

    async function handleCancelReject(){
      return useAsyncState($api.vacations.reject.cancel(props.vacation.id), [] as unknown as Api.Vacation, {
        onSuccess(res: Api.Vacation) {
          ctx.emit('status-vacation', res.status)
          window.connections.ws.value!.send(
            JSON.stringify({
              event: 'reject_cancel_request',
              request_id: props.vacation.id
            })
          )
        }
      })
    }

    function transformString(inputString: string): string {
      const words = inputString.split('_')
      const capitalizedWords = words.map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      const resultString = capitalizedWords.join(' ')
      return resultString
    }

    async function calculateActualDays() {
      return useAsyncState(
        $api.vacations.calculate.list({
          start_date: startDate.value.split(' ')[0].split('T')[0],
          end_date: endDate.value.split(' ')[0].split('T')[0]
        }),
        []
      )
    }

    watch([startDate, endDate], async([newStart, newEnd]) => {
      if (form.value) {
        await validateForm();
      }
      
      if (form.value?.isValid) {
        const START = startDate.value.split('T')[0].split(' ')[0]
        const END = endDate.value.split('T')[0].split(' ')[0]
        if (START === END) {
          const start = convertToTimeOnly(newStart);
          const end = convertToTimeOnly(newEnd);
          actualDays.value = calculateTimes(start, end)
        } else {
          actualDays.value = (await calculateActualDays()).state.value;
        }
      }
    })

    async function updateVacation() {
      const actualDays = await calculateActualDays()

      await useAsyncState(
        $api.vacations.edit.update(props.vacation.id, {
          reason: leaveReason.value.reason,
          from_date: startDate.value,
          end_date: endDate.value,
          actual_days: actualDays.state.value
        }),
        null,
        {
          onSuccess(data) {
            ctx.emit('update-vacation', data)
          }
        }
      )
    }

    return {
      startDate,
      disabled,
      endDate,
      leaveReason,
      leaveReasons,
      form,
      couldApprove,
      couldUpdate,
      couldDelete,
      user,
      actualDays,
      validateForm,
      validateEndDate,
      validateStartDate,
      updateVacation,
      handleApprove,
      handleReject,
      handleDelete,
      requestToCancel,
      capitalize,
      handleCancelApprove,
      handleCancelReject,
      formatRequestStatus,
      getStatusColor,
      formatDateTime,
    }
  }
}
</script>
