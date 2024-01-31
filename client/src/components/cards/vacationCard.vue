<template>
  <v-card elevation="0" >
    <v-card-title class="bg-graytitle">
      <div class="d-flex flex-row-reverse">
        <v-icon size="small" class="me-2" @click.stop="$emit('close-dialog', false)">
          mdi-close
        </v-icon>
      </div>
    </v-card-title>
    <v-card-title class="text-center">
      From <b color="primary">{{ vacation.from_date }} </b> to
      <b color="primary">{{ vacation.end_date }} </b> vacation</v-card-title
    >
    <br />

    <v-form ref="form" @submit.prevent="updateVacation()">
      <v-row class="d-flex flex-row-reverse" v-if="couldUpdate">
        <v-btn color="primary" class="ma-4" type="submit" :disabled="!form?.isValid || disabled">Update</v-btn>
        <v-btn color="red" class="ma-4" @click="handleDelete">Delete</v-btn>
      </v-row>
      <v-card elevation="0" class="pa-8">
        <v-row class="py-5">
          <v-col cols="3">
            <v-icon>mdi-account</v-icon>

            <b> Applying User</b>
          </v-col>
          <v-col cols="3" class="text-right">
            {{ vacation.user.full_name }}
          </v-col>

        </v-row>

        <v-row>
          <v-col cols="2">
            <v-icon>mdi-calendar</v-icon>

            <b> From</b>
          </v-col>
          <v-col cols="4">
            <v-text-field color="primary'" item-color="primary" base-color="primary" variant="outlined" hide-details="auto"
              label="From" v-model="startDate" :readonly="!couldUpdate" type="date">
            </v-text-field>
          </v-col>

          <v-col cols="2">
            <v-icon>mdi-calendar</v-icon>

            <b> To</b>
          </v-col>
          <v-col cols="4">
            <v-text-field color="primary'" item-color="primary" base-color="primary" variant="outlined" hide-details="auto"
              label="To" v-model="endDate" :readonly="!couldUpdate" type="date" :rules="[validateEndDate]">
            </v-text-field>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="2">
            <v-icon>mdi-navigation</v-icon>

            <b> Reason</b>
          </v-col>
          <v-col cols="4">
            <v-autocomplete color="primary" item-color="primary" base-color="primary" variant="outlined"
              v-model="leaveReason" :items="leaveReasons" label="Reason" return-object item-title="name"
              :readonly="!couldUpdate">
            </v-autocomplete>
          </v-col>
          <v-col cols="3">
            <v-icon>mdi-calendar</v-icon>
            <b> Status</b>
          </v-col>
          <v-col cols="3" class="text-right">
            {{ vacation.status }}
          </v-col>
        </v-row>
      </v-card>
    </v-form>

    <v-row v-if="couldApprove && vacation.status == 'pending'">
      <v-btn color="primary" class="ma-4" @click="handleApprove">Approve</v-btn>
      <v-btn color="red" class="ma-4" @click="handleReject">Reject</v-btn>
    </v-row>
  </v-card>
</template>
<script lang="ts">
import type { Api } from '@/types';
import { computed, ref, watch } from 'vue';

import { useApi } from '@/hooks'
import { useAsyncState } from '@vueuse/core'
import { ApiClientBase } from '@/clients/api/base'

export default {
  name: 'vacationCard',
  props: ['vacation'],
  emits: {
    'close-dialog': (item: Boolean) => item,
    'update-vacation': (item: any) => item,
    'delete-vacation': () => true,
    'status-vacation': (item: string) => item
  },

  setup(props, ctx) {
    const $api = useApi()

    const startDate = ref<Date>(props.vacation.from_date)
    const endDate = ref<Date>(props.vacation.end_date)
    const leaveReason = ref<Api.LeaveReason>({
      name: transformString(props.vacation.reason),
      reason: props.vacation.reason
    })
    const form = ref()
    const disabled = ref<boolean>(true)
    const user = ApiClientBase.user
    const leaveReasons = ref<Api.LeaveReason[]>([ ])

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

    const couldApprove = computed(() => {
      if (user.value) {
        if (
          user.value.fullUser.user_type === 'Admin' ||
          user.value.fullUser.user_type === 'Supervisor'
        ) {
          if (props.vacation.user.id == user.value.fullUser.id) {
            return true
          }
          if (
            props.vacation.user.reporting_to.includes(user.value.fullUser.id) &&
            props.vacation.user.location.name === user.value.fullUser.location.name
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
          start_date: startDate.value,
          end_date: endDate.value
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

      useAsyncState(
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
      validateEndDate,
      updateVacation,
      handleApprove,
      handleReject,
      handleDelete
    }
  }
}
</script>
