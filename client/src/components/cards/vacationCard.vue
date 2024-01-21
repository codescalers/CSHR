
<template>
  <v-card elevation="0" variant="outlined" color="white" class="pa-4">

    <v-icon class="me-2" @click.stop="$emit('close-dialog', false)"> mdi-close </v-icon>

    <v-card-title class="text-center"> From <b color="primary">{{ vacation.from_date }} </b> to <b color="primary">{{
      vacation.end_date }} </b> vacation</v-card-title>
    <br>

    <v-row v-if="vacation.status == 'pending' && state.user.value.id == vacation.applying_user">
      <v-btn color="primary" class="ma-4" @click="readOnly = false">Update</v-btn>
      <v-btn color="red" class="ma-4" @click="handleDelete" @click.stop="$emit('close-dialog', false)">Delete</v-btn>
    </v-row>

    <v-form ref="form" @submit.prevent="updateVacation()" @click.stop="$emit('close-dialog', false)">
      <v-card elevation="0" class="pa-8">
        <v-row class="py-5">
          <v-col cols="3">
            <v-icon>mdi-account</v-icon>

            <b> Applying User</b>

          </v-col>
          <v-col cols="3" class="text-right">
            {{ applyingUser?.full_name }}
          </v-col>

          <v-col cols="3">
            <v-icon>mdi-account</v-icon>

            <b> Approval User </b>

          </v-col>
          <v-col cols="3" class="text-right">
            {{ vacation.approval_user ? vacation.approval_user : "Under approving" }}
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="2">
            <v-icon>mdi-calendar</v-icon>

            <b> From</b>

          </v-col>
          <v-col cols="4">
            <v-text-field color="primar'" item-color="primary" base-color="primary" variant="outlined" hide-details="auto"
              label="From" v-model="startDate" :readonly="readOnly" type="date">
            </v-text-field>
          </v-col>

          <v-col cols="2">
            <v-icon>mdi-calendar</v-icon>

            <b> To</b>

          </v-col>
          <v-col cols="4">
            <v-text-field color="primar'" item-color="primary" base-color="primary" variant="outlined" hide-details="auto"
              label="To" v-model="endDate" :readonly="readOnly" type="date">
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
              :readonly="readOnly">
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
        <v-row>
          <v-col cols="12" v-if="!readOnly">
            <v-btn color="" class="ma-4" @click="readOnly = true">Cancel</v-btn>
            <v-btn color="primary" type="submit" :disabled="!form?.isValid" width="100%">
              Submit
            </v-btn>

          </v-col>
        </v-row>
      </v-card>
    </v-form>

    <v-row v-if="couldApprove">
      <v-btn color="red" class="ma-4" @click="handleReject" @click.stop="$emit('close-dialog', false)">Reject</v-btn>
      <v-btn color="primary" class="ma-4" @click="handleApprove"
        @click.stop="$emit('close-dialog', false)">Approve</v-btn>
    </v-row>

  </v-card>
</template>
<script lang="ts">
import type { Api } from '@/types';
import { computed, onMounted, ref } from 'vue';

import { useState } from '@/store'
import { $api } from '@/clients';

export default {
  name: "vacationCard",
  props: ["vacation"],
  emits: {
    'close-dialog': (item: Boolean) => item
  },

  setup(props) {
    const startDate = ref<Date>(props.vacation.from_date)
    const endDate = ref<Date>(props.vacation.end_date)
    const state = useState()

    const readOnly = ref<Boolean>(true)
    const couldApprove = computed(() => {
      if (state.user.value.user_type === 'Admin'
        || state.user.value.user_type === 'Supervisor'
      ) {
        if (applyingUser.value?.id == state.user.value.id) {
          return true;

        }
        if (applyingUser.value?.reporting_to.includes(state.user.value.id)
          && applyingUser.value?.location.name === state.user.value.location.name) {
          return true;
        }
        return false
      }

      return false
    });
    const leaveReason = ref<Api.LeaveReason>({ name: transformString(props.vacation.reason), reason: props.vacation.reason })
    const form = ref()
    const applyingUser = ref<Api.User>();




    const leaveReasons = ref<Api.LeaveReason[]>([{
      name: "Public Holidays",
      reason: "public_holidays"
    }, {
      name: "Emergency Leaves",
      reason: "emergency_leaves",
    }, {
      name: "Sick Leaves",
      reason: "sick_leaves",
    },
    {
      name: "Annual Leaves",
      reason: "annual_leaves",
    },
    {
      name: "Unpaid",
      reason: "unpaid",
    },
    {
      name: "Compensation",
      reason: "compensation",
    },
    ])
    async function getApplyingUser() {
      applyingUser.value = await $api.users.getuser(props.vacation.applying_user);
    }

    onMounted(async () => {
      await getApplyingUser()
    })

    async function handleDelete() {
      return await $api.vacations.delete(props.vacation.id)
    }
    async function handleApprove() {
      return await $api.vacations.approve.update(props.vacation.id
      )
    }
    async function handleReject() {
      return await $api.vacations.reject.update(props.vacation.id)
    }

    async function calculateActualDays() {
      return await $api.vacations.calculate.list({
        start_date: startDate.value,
        end_date: endDate.value,
      }
      )
    }
    function transformString(inputString: string): string {
      const words = inputString.split('_');
      const capitalizedWords = words.map(word => word.charAt(0).toUpperCase() + word.slice(1));
      const resultString = capitalizedWords.join(' ');

      return resultString;
    }


    async function updateVacation() {
      const actualDays = await calculateActualDays()
      await $api.vacations.edit.update(props.vacation.id,
        {
          reason: leaveReason.value.reason,
          from_date: startDate.value,
          end_date: endDate.value,
          actual_days: actualDays
        },
      )
    }


    return {
      startDate,
      endDate,
      leaveReason,
      leaveReasons,
      readOnly,
      form,
      state,
      applyingUser,
      couldApprove,
      updateVacation,
      handleApprove,
      handleReject,
      handleDelete,
    };
  },
};
</script>
