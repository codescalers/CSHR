
<template>
  <v-card elevation="0" variant="outlined" color="primary" class="pa-4">
    <div class="d-flex flex-row-reverse">
      <v-icon class="me-2" @click.stop="$emit('close-dialog', false)"> mdi-close </v-icon>
    </div>
    <div class="d-flex justify-center">
      <v-tabs v-model="tab" color="primary" >
      <v-tab v-for="tab in tabs" :key="tab" :value="tab"> {{ tab }}</v-tab>
    </v-tabs>
    </div>


    <v-window v-model="tab">
      <v-window-item value="Leave">
        <leaveRequest :dates="dates"></leaveRequest>
      </v-window-item>

      <v-window-item value="Meeting">
        <meetingRequest :dates="dates" />
      </v-window-item>

      <v-window-item value="Event">
        <eventRequest :dates="dates" />
      </v-window-item>
    </v-window>


  </v-card>
</template>
<script lang="ts">
import { ref } from 'vue';
import leaveRequest from '@/components/requests/leaveRequest.vue';
import eventRequest from './requests/eventRequest.vue';
import meetingRequest from './requests/meetingRequest.vue';


export default {
  name: "calenderRequest",
  props: ["dates"],
  components: {
    leaveRequest,
    eventRequest,
    meetingRequest,
  },
  emits: {
    'close-dialog': (item: Boolean) => item
  },
  setup(props) {
    const tabs = ["Leave", "Meeting", "Event"];
    const tab = ref<String>("")

    return {
      tab,
      tabs,
      leaveRequest,
      eventRequest,
      meetingRequest,
    };
  },
};
</script>
