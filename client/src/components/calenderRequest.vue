
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
        <leaveRequest :dates="dates" @create-event="createLeave()"></leaveRequest>
      </v-window-item>

      <v-window-item value="Meeting">
        <meetingRequest :dates="dates" @create-event="createMeeting()" />
      </v-window-item>

      <v-window-item value="Event">
        <eventRequest :dates="dates" @create-event="createEvent()"/>
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
    'close-dialog': (item: Boolean) => item,
    'update-vacation': () => true,
    'update-meeting': () => true,
    'update-event': () => true,
  },
  setup(props,ctx) {
    const tabs = ["Leave", "Meeting", "Event"];
    const tab = ref<String>("")
      async function createLeave() {
        ctx.emit("update-vacation")
    }

    async function createMeeting() {
        ctx.emit("update-meeting")
    }
    async function createEvent() {
        ctx.emit("update-event")
    }

    return {
      tab,
      tabs,
      leaveRequest,
      eventRequest,
      meetingRequest,
      createEvent,
      createLeave,
      createMeeting,
    };
  },
};
</script>
