
<template>
  <v-form ref="form" @submit.prevent="createLeave()">
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
        <v-btn color="primary" type="submit" :disabled="!form?.isValid || !isValid" width="100%" >
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


export default {
  name: "leaveRequest",
  props: ["dates"],
  emits: {
    'create-event': () => true,
  },
  setup(props, ctx) {
    const $api = useApi()
    const form = ref()
    const startDate = ref<Date>(props.dates.startStr)
    const endDate = ref<Date>(props.dates.endStr)
    const leaveReason = ref<Api.LeaveReason>()

    const isValid = computed(() => {
      let val = leaveReason.value ? true : false;
      return val;
    });


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

    async function calculateActualDays() {
      return await $api.vacations.calculate.list({
        start_date: startDate.value,
        end_date: endDate.value,
      }
      )
    }

    async function createLeave() {
      if (leaveReason.value) {
        calculateActualDays()
        useAsyncState($api.vacations.create(
          {
            reason: leaveReason.value.reason,
            from_date: startDate.value,
            end_date: endDate.value,
          },
        ), undefined , {
        onSuccess(){
          ctx.emit("create-event")
        }
      })}

    }

    return {
      startDate,
      endDate,
      leaveReasons,
      leaveReason,
      form,
      isValid,
      createLeave,
    };
  },
};
</script>
