
<template>
  <v-card elevation="0" variant="outlined" color="primary" class="pa-4">

    <v-icon class="me-2" @click.stop="$emit('close-dialog', false)"> mdi-close </v-icon>

    <div>{{ vacation }}</div>
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
