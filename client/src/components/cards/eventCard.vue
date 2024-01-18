<template>
  <v-card elevation="0" variant="outlined" color="white" class="pa-4">
    <v-icon class="me-2" @click.stop="$emit('close-dialog', false)"> mdi-close </v-icon>

    <v-card-title class="text-center">
      <b>{{ event.name }}</b>
    </v-card-title>
    <v-card elevation="0" variant="outlined" class="pa-4 ma-5">
      <v-row class="text-center">
        <v-col cols="6">
          <b>Description</b>

        </v-col>
        <v-col cols="6">
          {{ event.description ? event.description : "--" }}

        </v-col>
      </v-row>

      <v-row class="text-center">
        <v-col cols="6">
          <b>From Date</b>
        </v-col>
        <v-col cols="6">
          {{ fromDate }}

        </v-col>
      </v-row>

      <v-row class="text-center">
        <v-col cols="6">
          <b>To Date</b>
        </v-col>
        <v-col cols="6">
          {{ toDate }}
        </v-col>
      </v-row>


      <v-row class="text-center">
        <v-col cols="6">
          <b>From Time</b>
        </v-col>
        <v-col cols="6">
          {{ fromTime }}
        </v-col>
      </v-row>

      <v-row class="text-center">
        <v-col cols="6">
          <b>To Time</b>
        </v-col>
        <v-col cols="6">
          {{ toTime }}
        </v-col>
      </v-row>

    </v-card>
  </v-card>
</template>
<script lang="ts">
import { computed, ref } from 'vue';


export default {
  name: "eventCard",
  props: ["event"],
  emits: {
    'close-dialog': (item: Boolean) => item
  },


  setup(props) {
    const fromDateTime = new Date(props.event.from_date);

    const fromDate = ref<string>(fromDateTime.toISOString().split('T')[0]);
    const fromTime = ref<string>(fromDateTime.toISOString().split('T')[1].substring(0, 8));

    const toDateTime = new Date(props.event.end_date);

    const toDate = ref<string>(toDateTime.toISOString().split('T')[0]);
    const toTime = ref<string>(toDateTime.toISOString().split('T')[1].substring(0, 8));

    return {
      fromDate,
      fromTime,
      toDate,
      toTime,
    };
  },
};
</script>
