<template>
  <v-card elevation="0" variant="outlined" color="white" class="pa-4">
    <div class="d-flex flex-row-reverse">
      <v-icon class="me-2" @click.stop="$emit('close-dialog', false)"> mdi-close </v-icon>
    </div>
    <v-card-title class="text-center my-2">
      <h1>{{ holiday.location.country }}</h1>
    </v-card-title>
    <v-card elevation="0" variant="outlined" class="pa-4 mt-2">
      <v-row class="pa-2 ">
        <p>
          <b>{{ holiday.holiday_date }}</b> is a public holiday in <b>{{ holiday.location.country }}</b>, We hope you and
          your family have a peaceful and enjoyable holiday. Please be aware that our office in <b>{{
            holiday.location.country }}</b>, will be closed on
          this date. Thank you!
        </p>
      </v-row>

    </v-card>
  </v-card>
</template>
<script lang="ts">
import { ref } from 'vue';


export default {
  name: "holidayCard",
  props: ["holiday"],
  emits: {
    'close-dialog': (item: Boolean) => item
  },


  setup(props) {
    return {
    };
  },
};
</script>
