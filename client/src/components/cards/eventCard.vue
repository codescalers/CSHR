<template>
  <v-card elevation="0" variant="outlined" color="white" class="pa-4">
    <v-icon class="me-2" @click.stop="$emit('close-dialog', false)"> mdi-close </v-icon>

    <v-card-title class="text-center my-2">
      <b>{{ event.name }}</b>
    </v-card-title>
    <v-card elevation="0" variant="outlined" class="pa-4 mb-0">
      <v-row class="pa-2">
        <b>Description</b>
      </v-row>
      <v-row class="pa-2">
        {{ event.description ? event.description : "--" }}
      </v-row>
    </v-card>
    <v-card elevation="0" variant="outlined" color="white" class="px-4">
      <v-row class="text-center mx-2 mt-2 ">
        <v-col cols="3" class="mt-2 border" v-for="header in Headers" :key="header">
          {{ header }}

        </v-col>
      </v-row>

      <v-row class="text-center mx-2 mb-2">

        <v-col cols="3" class="border">
          {{ fromDate }}
        </v-col>

        <v-col cols="3" class="border">
          {{ toDate }}
        </v-col>

        <v-col cols="3" class="border">
          {{ fromTime }}
        </v-col>

        <v-col cols="3" class="border">
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
    const Headers = ref(["From Date", "To Date", "From Time", "To Time"]);

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
      Headers,
    };
  },
};
</script>
