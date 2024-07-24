<template>
  <v-form ref="form" @submit.prevent="createMeeting()">
    <div class="mt-3">
      <v-text-field
        color="info"
        item-color="info"
        base-color="info"
        variant="outlined"
        hide-details="auto"
        label="Start Date"
        v-model="startDate"
        :readonly="true"
      >
        <template v-slot:append>
          <v-icon color="info">mdi-calendar</v-icon>
        </template>
      </v-text-field>
    </div>

    <div class="mt-3">
      <v-text-field
        item-color="info"
        base-color="info"
        color="info"
        variant="outlined"
        label="Meeting Link"
        v-model="meetingLink"
        hide-details="auto"
        :rules="[...fieldRequired, validURL]"
      >
      </v-text-field>
    </div>
    <div class="mt-3">
      <v-text-field
        item-color="info"
        base-color="info"
        color="info"
        variant="outlined"
        label="Meeting Location"
        v-model="location"
        hide-details="auto"
        :rules="fieldRequired"
      >
      </v-text-field>
    </div>

    <div class="mt-3">
      <v-text-field
        item-color="info"
        base-color="info"
        color="info"
        variant="outlined"
        label="Meeting Time"
        v-model="meetingTime"
        hide-details="auto"
        :rules="fieldRequired"
        type="time"
      >
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
import { computed, ref } from 'vue'
import { fieldRequired, validURL } from '@/utils'
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
    const startDate = ref<any>(props.dates.startStr)
    const meetingLink = ref<string>('')
    const location = ref<string>('')
    const form = ref()
    const meetingTime = ref()
    const requesting = ref<boolean>(false)

    const meetingDateTime = computed(() => {
      let val = new Date(startDate.value)
      if (startDate.value) {
        const [hours, minutes] = meetingTime.value.split(':').map(Number)
        val.setHours(hours, minutes, 0, 0)
      }

      return val.toISOString()
    })

    async function createMeeting() {
      requesting.value = true
      await useAsyncState(
        $api.meeting.create({
          date: meetingDateTime.value,
          meeting_link: meetingLink.value,
          location: location.value
        }),
        undefined,
        {
          onSuccess(data) {
            ctx.emit('create-event', data)
          }
        }
      )
      requesting.value = false
    }

    return {
      startDate,
      meetingLink,
      location,
      form,
      meetingTime,
      requesting,
      fieldRequired,
      validURL,
      createMeeting
    }
  }
}
</script>
