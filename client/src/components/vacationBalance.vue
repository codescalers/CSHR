<template>

  shjshjdjhdjhdj
  <v-card>
    <v-card-title class="font-weight-bold bg-primary">Vacation Balance</v-card-title>
            <v-row class=" text-center mt-2 mb-0">
              <v-col v-for="header in vacationInfoHeaders" :key="header">
               <h4> {{ header }}</h4> 
              </v-col>
            </v-row>
            <v-row class=" text-center mt-0 mb-2">
              <v-col>
                {{ name }} / {{ name }}
              </v-col>
              <v-col>
                {{ name }} / {{ name }}
              </v-col>
              <v-col>
                {{ name }} / {{ name }}
              </v-col>
            </v-row>
  </v-card>
</template>

<script lang="ts">
import { ref } from 'vue';

export default {
  name: 'vacationBalance',
  setup() {
    const name = ref<string>('mayar osama')
    const vacationInfoHeaders = ["Annuals", "Emergencies", "Excuses"];

    return {
      name,
      vacationInfoHeaders,
    }
  }
}
</script>

