
<template>
  <v-card elevation="0" variant="outlined" color="white" class="pa-4">
    <v-icon class="me-2" @click.stop="$emit('close-dialog', false)"> mdi-close </v-icon>

    <v-card-title class="text-center">
      Meeting Created by
      <br>
      <b>{{ meeting.host_user.full_name }}</b>
    </v-card-title>
    <v-card elevation="0" variant="outlined" class="pa-4 ma-5">
      <v-row class="text-center">
        <v-col cols="6">
          <b>Team</b>

        </v-col>
        <v-col cols="6">
          {{ meeting.host_user.team ? meeting.host_user.team : "--" }}

        </v-col>
      </v-row>

      <v-row class="text-center">
        <v-col cols="6">
          <b>Meeting Link</b>
        </v-col>
        <v-col cols="6">
          <a :href="meeting.meeting_link"><v-icon class="me-2"> mdi-link </v-icon>Meeting Link</a>
        </v-col>
      </v-row>

      <v-row class="text-center">
        <v-col cols="6">
          <b>Date</b>
        </v-col>
        <v-col cols="6">
          {{ date }}
        </v-col>
      </v-row>


      <v-row class="text-center">
        <v-col cols="6">
          <b>Time</b>
        </v-col>
        <v-col cols="6">
          {{ time }}
        </v-col>
      </v-row>

    </v-card>
  </v-card>
</template>
<script lang="ts">
import { ref } from 'vue';



export default {
  name: "meetingCard",
  props: ["meeting"],
  emits: {
    'close-dialog': (item: Boolean) => item
  },

  setup(props) {

    const dateTime = new Date(props.meeting.date);

    const date = ref<string>(dateTime.toISOString().split('T')[0]);
    const time = ref<string>(dateTime.toISOString().split('T')[1].substring(0, 8));

    return {
      date,
      time,
    };
  },
};
</script>
