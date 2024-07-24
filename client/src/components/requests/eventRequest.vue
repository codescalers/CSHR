<template>
  <v-form ref="form" @submit.prevent="createEvent()">
    <div class="mt-3">
      <v-text-field
        ref="startDateField"
        color="info"
        item-color="info"
        base-color="info"
        variant="outlined"
        hide-details="auto"
        label="From"
        v-model="startDate"
        type="date"
        :rules="[validateDates]"
      ></v-text-field>
    </div>

    <div class="mt-3">
      <v-text-field
        ref="endDateField"
        color="info"
        item-color="info"
        base-color="info"
        variant="outlined"
        hide-details="auto"
        label="To"
        v-model="endDate"
        type="date"
        :rules="[validateDates]"
      ></v-text-field>
    </div>

    <div class="mt-3">
      <v-text-field item-color="info" base-color="info" color="info" variant="outlined" label="Event Name" v-model="name"
        hide-details="auto" :rules="fieldRequired">
      </v-text-field>
    </div>
    <div class="mt-3">
      <v-text-field item-color="info" base-color="info" color="info" variant="outlined" label="Description"
        v-model="description" hide-details="auto" :rules="fieldRequired">
      </v-text-field>
    </div>

    <div class="mt-3">
      <v-text-field item-color="info" base-color="info" color="info" variant="outlined" label="Event Start Time"
        v-model="eventStart" hide-details="auto" :rules="[...fieldRequired, validateTimes]" type="time">
      </v-text-field>
    </div>

    <div class="mt-3">
      <v-text-field item-color="info" base-color="info" color="info" variant="outlined" label="Event End Time"
        v-model="eventEnd" hide-details="auto" :rules="[...fieldRequired, validateTimes]" type="time">
      </v-text-field>
    </div>

    <v-row class="mt-3 pa-4 d-flex justify-end">
      <v-btn
        color="primary"
        type="submit"
        :disabled="!form?.isValid || requesting"
        :loading="requesting"
      >
        Submit
      </v-btn>
    </v-row>
  </v-form>
</template>
<script lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { fieldRequired } from '@/utils'
import { useApi } from '@/hooks'
import { useAsyncState } from '@vueuse/core'

export default {
  name: 'leaveRequest',
  props: ['dates'],
  emits: {
    'create-event': (item: any) => item
  },
  setup(props, ctx) {
    const $api = useApi()
    const startDate = ref<string>(props.dates.startStr)
    const endDate = ref<any>(new Date(props.dates.endStr))
    endDate.value.setDate(endDate.value.getDate() - 1);
    endDate.value = endDate.value.toISOString().split('T')[0];
    const name = ref<string>("")
    const description = ref<string>("")
    const form = ref()
    const eventStart = ref('08:00')
    const eventEnd = ref('16:00')
    const startDateField = ref()
    const endDateField = ref()
    const requesting = ref<boolean>(false)

    watch(
      () => [startDate.value, endDate.value],
      async () => {
        setTimeout(async () => {
          startDateField.value.validate();
          endDateField.value.validate();
        }, 200);
      },
    );


    const validateDates = (): string | boolean => {
      if (!startDate.value) return 'Please select start date.'
      if (!endDate.value) return 'Please select end date.'
      if (endDate.value < startDate.value) return 'End date must be after start date.'
      return true
    }

    const validateTimes = (): string | boolean => {
      if (!eventEnd.value) return 'Please select end time.'
      if (eventEnd.value < eventStart.value) return 'End time must be after start time.'
      return true
    }

    onMounted(async () => {
      startDateField.value.validate()
      endDateField.value.validate()
     
    })
    async function createEvent() {
      requesting.value = true;
      await useAsyncState(
        $api.event.create({
          name: name.value,
          description: description.value,
          from_date: `${startDate.value}T${eventStart.value}`,
          end_date: `${endDate.value}T${eventEnd.value}`,
        }),
        undefined,
        {
          onSuccess(data) {
            ctx.emit('create-event', data)
          }
        }
      )
      requesting.value = false;
    }

    return {
      startDate,
      endDate,
      name,
      description,
      form,
      fieldRequired,
      eventStart,
      eventEnd,
      requesting,
      startDateField,
      endDateField,
      validateDates,
      createEvent,
      validateTimes,
    }
  }
}
</script>
