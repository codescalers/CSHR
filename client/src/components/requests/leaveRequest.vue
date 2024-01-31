
<template>
  <v-form ref="form" @submit.prevent="createLeave()">
    <v-alert density="compact" class="pa-5 my-5" type="warning">
      {{ actualDays.state.value === 0 ? "Actual vacation days requested is zero, Selected days might include weekends or public holidays" : "Actual vacation days requested are " + actualDays.state.value +" days" }}
    </v-alert>

    <div class="mt-3">
      <v-text-field color="primar'" item-color="primary" base-color="primary" variant="outlined" hide-details="auto"
        label="From" v-model="startDate" :readonly="true">
        <template v-slot:append>
          <v-icon color="primary">mdi-calendar</v-icon>
        </template>
      </v-text-field>
    </div>

    <div class="mt-3">

      <v-text-field color="primary" item-color="primary" base-color="primary" :readonly="true" variant="outlined"
        v-model="endDate" hide-details="auto" label="To">
        <template v-slot:append>
          <v-icon color="primary">mdi-calendar</v-icon>
        </template>
      </v-text-field>
    </div>

    <div class="mt-3">

      <v-autocomplete color="primary" item-color="primary" base-color="primary" variant="outlined" v-model="leaveReason"
        :items="leaveReasons" label="Reason" return-object item-title="name">
      </v-autocomplete>

    </div>

    <v-row class="mt-3 d-flex flex-row-reverse">

      <v-col cols="3">
        <v-btn color="primary" type="submit" :disabled="!form?.isValid || !isValid || actualDays.state.value === 0"
          width="100%">
          Submit
        </v-btn>
      </v-col>
    </v-row>
  </v-form>
</template>
<script lang="ts">
import { useApi } from '@/hooks'
import type { Api } from '@/types';
import { useAsyncState } from '@vueuse/core';
import { computed, ref } from 'vue';
// import { useState } from '@/store'
import { ApiClientBase } from '@/clients/api/base';

export default {
  name: "leaveRequest",
  props: ["dates"],
  emits: {
    'create-event': (item: any) => item,
  },
  setup(props, ctx) {
    // const state = useState()
    const $api = useApi()
    const form = ref()
    const startDate = ref<Date>(props.dates.startStr)
    const endDate = ref<Date>(props.dates.endStr)
    const user = ApiClientBase.user
    const leaveReason = ref<Api.LeaveReason>()
    const actualDays = useAsyncState($api.vacations.calculate.list({
      start_date: startDate.value,
      end_date: endDate.value,
    }), [])

    const isValid = computed(() => {
      let val = leaveReason.value ? true : false;
      return val;
    });
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

    async function createLeave() {
      if (leaveReason.value) {
        useAsyncState($api.vacations.create(
          {
            reason: leaveReason.value.reason,
            from_date: startDate.value,
            end_date: endDate.value,
          },
        ), undefined, {
          onSuccess(data) {
            ctx.emit("create-event", data)
          }
        })
      }

    }

    return {
      startDate,
      endDate,
      leaveReasons,
      leaveReason,
      form,
      isValid,
      actualDays,
      user,
      createLeave,
    };
  },
};
</script>
