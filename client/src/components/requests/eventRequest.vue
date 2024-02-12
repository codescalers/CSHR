<template>
  <v-form ref="form" @submit.prevent="createEvent()">
    <div class="mt-3">
      <v-text-field ref="startDateField" color="info" item-color="info" base-color="info" variant="outlined"
        hide-details="auto" label="From" v-model="startDate" type="date" :rules="[validateDates]"></v-text-field>
    </div>

    <div class="mt-3">
      <v-text-field ref="endDateField" color="info" item-color="info" base-color="info" variant="outlined"
        hide-details="auto" label="To" v-model="endDate" type="date" :rules="[validateDates]"></v-text-field>
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
        v-model="eventStart" hide-details="auto" :rules="fieldRequired" type="time">
      </v-text-field>
    </div>

    <div class="mt-3">
      <v-text-field item-color="info" base-color="info" color="info" variant="outlined" label="Event End Time"
        v-model="eventEnd" hide-details="auto" :rules="fieldRequired" type="time">
      </v-text-field>
    </div>

    <v-row class="mt-3 pa-4 d-flex justify-end">
      <v-btn color="primary" type="submit" :disabled="!form?.isValid"> Submit </v-btn>
    </v-row>
  </v-form>
</template>
<script lang="ts">
import { computed, ref, watch } from 'vue'
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
    const eventStart = ref()
    const eventEnd = ref()
    const startDateField = ref()
    const endDateField = ref()

    watch(
      () => [startDate.value, endDate.value],
      async () => {
        setTimeout(async () => {
          startDateField.value.validate();
          endDateField.value.validate();
        }, 200);
      },
    );


    const validateDates = (value: string | null): string | boolean => {
      if (!startDate.value) return 'Please select start date.';
      if (!endDate.value) return 'Please select end date.';
      if (endDate.value <= startDate.value) return 'End date must be after start date.';
      return true;
    };
    const from_date = computed(() => {
      let val = new Date(startDate.value)
      if (eventStart.value) {
        const [hours, minutes] = eventStart.value.split(':').map(Number)
        val.setHours(hours, minutes, 0, 0)
      }

      return val.toISOString()
    })
    const end_date = computed(() => {
      let val = new Date(endDate.value)
      if (eventEnd.value) {
        const [hours, minutes] = eventEnd.value.split(':').map(Number)
        val.setHours(hours, minutes, 0, 0)
      }

      return val.toISOString()
    })

    async function createEvent() {
      useAsyncState(
        $api.event.create({
          name: name.value,
          description: description.value,
          from_date: from_date.value,
          end_date: end_date.value
        }),
        undefined,
        {
          onSuccess(data) {
            ctx.emit('create-event', data)
          }
        }
      )
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
      startDateField,
      endDateField,
      validateDates,
      createEvent
    }
  }
}
</script>
