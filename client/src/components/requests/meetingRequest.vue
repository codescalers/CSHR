
<template>
  <v-form ref="form" @submit.prevent="createMeeting()">



    <div class="mt-3">
      <v-text-field color="primar'" item-color="primary" base-color="primary" variant="outlined" hide-details="auto"
        label="Start Date" v-model="startDate" :readonly="true">
        <template v-slot:append>
          <v-icon color="primary">mdi-calendar</v-icon>
        </template>
      </v-text-field>
    </div>



    <div class="mt-3">

      <v-text-field item-color="primary" base-color="primary" color="primary" variant="outlined" label="Meeting Link"
        v-model="meetingLink" hide-details="auto" :rules="fieldRequired">
        <!-- <template v-slot:append>
          <v-icon color="primary">mdi-domain</v-icon>
        </template> -->
      </v-text-field>
      <!-- 
        <v-text-field color="primary" item-color="primary" base-color="primary" :readonly="true" variant="outlined"
          v-model="name" label="Name" :rules="fieldRequired">

        </v-text-field> -->
    </div>
    <div class="mt-3">

      <v-text-field item-color="primary" base-color="primary" color="primary" variant="outlined" label="Meeting Location"
        v-model="location" hide-details="auto" :rules="fieldRequired">
        <!-- <template v-slot:append>
          <v-icon color="primary">mdi-domain</v-icon>
        </template> -->
      </v-text-field>
    </div>



    <div class="mt-3">
      <v-text-field item-color="primary" base-color="primary" color="primary" variant="outlined" label="Meeting Time"
        v-model="meetingTime" hide-details="auto" :rules="fieldRequired" type="time">
        <!-- <template v-slot:append>
<v-icon color="primary">mdi-domain</v-icon>
</template> -->
      </v-text-field>
    </div>
    <v-row class="mt-3">

      <v-col cols="3">
        <v-btn color="primary" type="submit" :disabled="!form?.isValid" width="100%">
          Submit
        </v-btn>
      </v-col>
    </v-row>
  </v-form>
</template>
<script lang="ts">
import { computed, ref } from 'vue';
import { fieldRequired } from '@/utils';
import { $api } from '@/clients';
import { useRouter } from 'vue-router';
import { set } from 'date-fns';


export default {
  name: "leaveRequest",
  props: ["dates"],

  setup(props) {
    const startDate = ref<any>(props.dates.startStr)
    const meetingLink = ref<string>("")
    const location = ref<string>("")
    const form = ref()
    const $router = useRouter()
    const meetingTime = ref()

    const meetingDateTime = computed(() => {
      let val = new Date(startDate.value);
      if (startDate.value) {
        const [hours, minutes] = meetingTime.value.split(':').map(Number);
        val.setHours(hours, minutes, 0, 0);
      }

      return val.toISOString();
    });
   

    async function createMeeting() {
      await $api.meeting.create(
        {
          date: meetingDateTime.value,
          meeting_link: meetingLink.value,
          location: location.value,
        },
      )
    }

    return {
      startDate,
      meetingLink,
      location,
      form,
      meetingTime,
      fieldRequired,
      createMeeting,
    };
  },
};
</script>
