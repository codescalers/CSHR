
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

    <v-row class="mt-3">

      <v-col cols="3">
        <v-btn color="primary" type="submit" :disabled="!form?.isValid || !isValid" width="100%">
          Submit
        </v-btn>
      </v-col>
    </v-row>
  </v-form>
</template>
<script lang="ts">
import { $api } from '@/clients';
import type { Api } from '@/types';
import { computed, ref } from 'vue';


export default {
  name: "leaveRequest",
  props: ["dates"],

  setup(props) {
    const form = ref()
    const startDate = ref<any>(props.dates.startStr)
    const endDate = ref<any>(props.dates.endStr)
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

    function getDaysBetweenDates(date1: Date, date2: Date): number {

      const timeDifference = Math.abs(date2.getTime() - date1.getTime());
      const daysDifference = Math.ceil(timeDifference / (1000 * 3600 * 24));
      return daysDifference;
    }

    async function createLeave() {
      if (leaveReason.value) {
        await $api.vacations.create(
          {
            reason: leaveReason.value?.reason,
            from_date: startDate.value,
            end_date: endDate.value,
            actual_days: getDaysBetweenDates(props.dates.start, props.dates.start),

          },
        )
      }

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
