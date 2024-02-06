<template>
  <v-form ref="form" @submit.prevent="createLeave()">
    <v-alert density="compact" class="pa-5 my-5" type="warning">
      {{ actualDays.state.value === 0 ? "Actual vacation days requested is zero, Selected days might include weekends or public holidays" : "Actual vacation days requested are " + actualDays.state.value +" days" }}
    </v-alert>

    <div class="mt-3">
      <v-text-field ref="startDateField" color="info" item-color="info" base-color="info" variant="outlined"
        hide-details="auto" label="From" v-model="startDate" type="date" :rules="[validateDates]"></v-text-field>
    </div>

    <div class="mt-3">
      <v-text-field ref="endDateField" color="info" item-color="info" base-color="info" variant="outlined"
        hide-details="auto" label="To" v-model="endDate" type="date" :rules="[validateDates]"></v-text-field>
    </div>
    <div class="mt-3">
      <v-autocomplete color="info" item-color="info" base-color="info" variant="outlined" v-model="leaveReason"
        :items="leaveReasons" label="Reason" return-object item-title="name">
      </v-autocomplete>
    </div>
    <v-row class="pa-4 d-flex justify-end">
      <v-btn color="primary" type="Submit" :disabled="!form?.isValid || !isValid || actualDays.state.value === 0"> Submit
      </v-btn>
    </v-row>
  </v-form>
</template>
<script lang="ts">
import { useApi } from '@/hooks'
import type { Api } from '@/types';
import { useAsyncState } from '@vueuse/core';
import { computed, ref, watch } from 'vue';
import { ApiClientBase } from '@/clients/api/base';

export default {
  name: 'leaveRequest',
  props: ['dates'],
  emits: {
    'create-event': (item: any) => item
  },
  setup(props, ctx) {
    const $api = useApi()
    const form = ref()
    const startDateField = ref()
    const endDateField = ref()
    const startDate = ref<Date>(props.dates.startStr)
    const endDate = ref<any>(new Date(props.dates.endStr))
    endDate.value.setDate(endDate.value.getDate() - 1);
    endDate.value = endDate.value.toISOString().split('T')[0];
    const user = ApiClientBase.user
    const leaveReason = ref<Api.LeaveReason>()

    const actualDays = useAsyncState(
      async () => {
        return $api.vacations.calculate.list({
          start_date: startDate.value,
          end_date: endDate.value,
        })
      },
      undefined,

    )

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


    watch(
      () => [startDate.value, endDate.value],
      async () => {
        setTimeout(async () => {
          console.log(startDateField.value.validate(), "hereeee")

          startDateField.value.validate();
          endDateField.value.validate();
          actualDays.execute();
        }, 200);
      },
    );

    const validateDates = (value: string | null): string | boolean => {
      if (!startDate.value) return 'Please select start date.';
      if (!endDate.value) return 'Please select end date.';
      if (endDate.value <= startDate.value) return 'End date must be after start date.';
      return true;
    };

    async function createLeave() {
      if (leaveReason.value) {
        useAsyncState($api.vacations.create(
          {
            reason: leaveReason.value.reason,
            from_date: startDate.value,
            end_date: endDate.value
          }),
          undefined,
          {
            onSuccess(data) {
              ctx.emit('create-event', data)
            }
          }
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
      actualDays,
      user,
      startDateField,
      endDateField,
      createLeave,
      validateDates,
    };
  },
};
</script>
