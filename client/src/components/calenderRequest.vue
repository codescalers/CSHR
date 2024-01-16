
<template>
  <v-card elevation="0" variant="outlined" color="primary" class="pa-4">
    <v-tabs v-model="tab" color="primary">
      <v-tab value="one">Leave</v-tab>
      <v-tab value="two">Meeting</v-tab>
      <v-tab value="three">Event</v-tab>
    </v-tabs>

    <v-window v-model="tab">
      <v-window-item value="one">
        <leaveRequest :dates="dates"></leaveRequest>
      </v-window-item>

      <v-window-item value="two">
        Two
      </v-window-item>

      <v-window-item value="three">
        <eventRequest :dates="dates"/>
      </v-window-item>
    </v-window>


  </v-card>
</template>
<script lang="ts">
import { ref } from 'vue';
import leaveRequest from '@/components/requests/leaveRequest.vue';
import eventRequest from './requests/eventRequest.vue';


export default {
  name: "calenderRequest",
  props: ["dates"],
  components: {
    leaveRequest,
    eventRequest,
  },
  // emits: {
  //   'close-dialogue': (item: Object) => item
  // },

  setup(props) {
    // const emit = defineEmits(['close-dialogue', 'update:request']);

    const tab = ref<String>("")



    return {
      tab,
      leaveRequest,
      eventRequest,
      // cshrDialogue,
      // emit,
    };
  },
};
</script>
