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
        From <b>{{ vacation.from_date }} </b> to
        <b color="primary">{{ vacation.end_date }} </b> vacation

      </p>

      <v-form ref="form" @submit.prevent="updateVacation()">
        <v-row class="d-flex justify-center my-2">
          <v-btn color="primary" v-if="couldUpdate" class="mx-1 my-2" type="submit"
            :disabled="!form?.isValid || disabled">Update</v-btn>
          <v-btn v-if="couldDelete" color="error" class="mx-1 my-2" @click="handleDelete">Delete</v-btn>
        </v-row>
        <v-divider class="my-2"></v-divider>

        <v-card elevation="0" class="pa-4">
          <v-row class="py-2">
            <v-col cols="6" class="d-flex">
              <v-icon class="mr-2">mdi-account</v-icon>
              <p>
                Applying User :
                <span color="warning" class="mx-2">{{
                  vacation.applying_user.full_name
                }}</span>
              </p>
            </v-col>
            <v-col cols="6" class="d-flex items-center">
              <p>
                Status :
                {{ vacation.status }}
              </p>
            </v-col>

          </v-row>

          <v-row>
            <v-col cols="6">
              <v-text-field color="info" item-color="info" base-color="info" variant="outlined" hide-details="auto"
                label="From" v-model="start_date" :readonly="!couldUpdate" type="date">
              </v-text-field>
            </v-col>
            <v-col cols="6">
              <v-text-field color="info" item-color="info" base-color="info" variant="outlined" hide-details="auto"
                label="To" v-model="end_date" :readonly="!couldUpdate" type="date" :rules="[validateEndDate]">
              </v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="6">
              <v-autocomplete color="info" item-color="info" base-color="info" variant="outlined" v-model="leaveReason"
                :items="leaveReasons" label="Reason" return-object item-title="name" :readonly="!couldUpdate">
              </v-autocomplete>
            </v-col>
          </v-row>

        </v-card>
      </v-form>
      <v-divider class="my-2"></v-divider>
      <v-row class="d-flex justify-end mt-3" v-if="couldApprove && vacation.status == 'pending'">
        <v-btn color="primary" class="ma-1" @click="handleApprove">Approve</v-btn>
        <v-btn color="error" class="ma-1" @click="handleReject">Reject</v-btn>
      </v-row>
    </v-container>
  </v-card>
</template>
<script lang="ts">
import type { Api } from '@/types';
import { computed, ref, watch } from 'vue';

import { useApi } from '@/hooks'
import { useAsyncState } from '@vueuse/core'
import { ApiClientBase } from '@/clients/api/base'
import type { PropType } from 'vue';

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
    'delete-vacation': () => true,
    'status-vacation': (item: string) => item
  },

  setup(props, ctx) {
    const $api = useApi()
    const startDate = ref<Date>(new Date(props.vacation.from_date));
     const start_date=  ref(startDate.value.toISOString().split('T')[0]);


    const endDate = ref<Date>(new Date(props.vacation.end_date))
      const end_date=  ref(endDate.value.toISOString().split('T')[0]);

    const leaveReason = ref<Api.LeaveReason>({
      name: transformString(props.vacation.reason),
      reason: props.vacation.reason
    })
    const form = ref()
    const disabled = ref<boolean>(true)
    const user = ApiClientBase.user
    const leaveReasons = ref<Api.LeaveReason[]>([])

    const balance = useAsyncState($api.vacations.getVacationBalance({ "user_ids": user.value?.fullUser.id }), null, {
      onSuccess(data: any) {
        leaveReasons.value = [{
          name: `Emergency Leaves  ${data[0].emergency_leaves.reserved} / ${data[0].emergency_leaves.all}`,
          reason: "emergency_leaves",
        }, {
          name: `Sick Leaves  ${data[0].sick_leaves.reserved} / ∞`,
          reason: "sick_leaves",
        },
        {
          name: `Annual Leaves  ${data[0].annual_leaves.reserved} / ${data[0].annual_leaves.all}`,
          reason: "annual_leaves",
        },
        {
          name: `Unpaid ${data[0].unpaid.reserved} / ∞`,
          reason: "unpaid",
        },
        {
          name: `Compensation  ${data[0].compensation.reserved} / ∞`,
          reason: "compensation",
        },]

      }
    })
    const couldUpdate = computed(() => {
      if (user.value) {
        if (props.vacation.status == 'pending') {
          // could update if user signed in is the same user applied for vacation
          if (props.vacation.isUpdated && user.value.fullUser.id == props.vacation.applying_user) {
            return true
          }
          if (
            !props.vacation.isUpdated &&
            user.value.fullUser.id == props.vacation.applying_user.id
          ) {
            return true
          }
          return false
        }
      }
      return false
    })

    const from_date = computed(() => {
      let val = new Date(startDate.value)
        val.setHours(8, 0, 0, 0)
      return val.toISOString()
    })
    const to_date = computed(() => {
      let val = new Date(endDate.value)
        val.setHours(16, 0, 0, 0)

      return val.toISOString()
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
          user.value.fullUser.user_type ==="Admin"&&
          props.vacation.applying_user.location.name === user.value.fullUser.location.name
        ) {
          return true
        }
        return false
      }
      return false
    })


    const couldApprove = computed(() => {

      if (user.value) {
        // only admins or supervisors could approve vacation
        if (
          user.value.fullUser.user_type === 'Admin' ||
          user.value.fullUser.user_type === 'Supervisor'
        ) {
          // Could approve if user signed in is the same user applied for vacation
          if (props.vacation.applying_user.id == user.value.fullUser.id) {
            return true
          }
          // Could approve if applying user reports to the supervisor or admin logged in 
          // and works from the same office
          if (
            props.vacation.applying_user.reporting_to &&
            props.vacation.applying_user.reporting_to[0]?.id === props.vacation.applying_user?.id &&
            props.vacation.applying_user.location.name === user.value.fullUser.location.name
          ) {
            return true
          }
          return false
        }
      }
      return false
    });

    watch([leaveReason, startDate, endDate], ([newLeaveReason, newStartDate, newEndDate], [oldLeaveReason, oldStartDate, oldEndDate]) => {
      if (newLeaveReason.name !== oldLeaveReason.name || newStartDate !== oldStartDate || newEndDate !== oldEndDate) {
        disabled.value = false;
        return
      }
      disabled.value = true;

    });

    function validateEndDate(value: any) {
      if (startDate.value && value <= startDate.value) {
        return 'To date must be after From date'
      }
      return true
    }
    async function handleDelete() {
      return useAsyncState($api.vacations.delete(props.vacation.id), [], {
        onSuccess() {
          ctx.emit('delete-vacation')
        }
      })
    }
    async function handleApprove() {
      return useAsyncState($api.vacations.approve.update(props.vacation.id), [], {
        onSuccess() {
          ctx.emit('status-vacation', 'Approve')
        }
      })
    }
    async function handleReject() {
      return useAsyncState($api.vacations.reject.update(props.vacation.id), [], {
        onSuccess() {
          ctx.emit('status-vacation', 'Reject')
        }
      })
    }

    async function calculateActualDays() {
      return useAsyncState(
        $api.vacations.calculate.list({
          start_date: start_date.value,
          end_date: end_date.value
        }),
        []
      )
    }
    function transformString(inputString: string): string {
      const words = inputString.split('_')
      const capitalizedWords = words.map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      const resultString = capitalizedWords.join(' ')
      return resultString
    }

    async function updateVacation() {
      const actualDays = await calculateActualDays()

      await useAsyncState(
        $api.vacations.edit.update(props.vacation.id, {
          reason: leaveReason.value.reason,
          from_date: from_date.value,
          end_date: to_date.value,
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
      start_date,
      end_date,
      validateEndDate,
      updateVacation,
      handleApprove,
      handleReject,
      handleDelete
    }
  }
}
</script>
