
<template>
  <v-card elevation="0" variant="outlined" color="white" class="pa-4">

    <v-icon class="me-2" @click.stop="$emit('close-dialog', false)"> mdi-close </v-icon>

    <v-card-title class="text-center"> From <b color="primary">{{ vacation.from_date }} </b> to <b color="primary">{{
      vacation.end_date }} </b> vacation</v-card-title>
    <br>
    <v-card elevation="0" class="pa-8">
      <v-row>
        <v-col cols="3">
          <v-icon>mdi-calendar</v-icon>

          <b> From</b>

        </v-col>
        <v-col cols="3" class="text-right">

          {{ vacation.from_date }}

        </v-col>
        <v-col cols="3">
          <v-icon>mdi-calendar</v-icon>
          <b> To</b>
        </v-col>
        <v-col cols="3" class="text-right">
          {{ vacation.end_date }}
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="3">
          <v-icon>mdi-navigation</v-icon>

          <b> Reason</b>

        </v-col>
        <v-col cols="3" class="text-right">

          {{ vacation.reason }}

        </v-col>
        <v-col cols="3">
          <v-icon>mdi-calendar</v-icon>
          <b> Status</b>
        </v-col>
        <v-col cols="3" class="text-right">
          {{ vacation.status }}
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-btn color="Primary">
            View
          </v-btn>
        </v-col>
      </v-row>
    </v-card>

    <v-btn color="red" class="ma-4">Reject</v-btn>
    <v-btn color="primary" class="ma-4">Approve</v-btn>



  </v-card>
</template>
<script lang="ts">
import { computed, ref } from 'vue';


export default {
  name: "vacationCard",
  props: ["vacation"],
  emits: {
    'close-dialog': (item: Boolean) => item
  },

  setup(props) {


    return {

    };
  },
};
</script>
