<template>
  <v-card>
    <v-card-title class="font-weight-medium bg-primary">Vacation Balance</v-card-title>
    <v-row class="text-center mt-2 mb-0">
      <v-col v-for="header in vacationInfoHeaders" :key="header">
        <h4>{{ header }}</h4>
      </v-col>
    </v-row>
    <v-row class="text-center mt-0 mb-2">
      <v-col>
        {{ balance ? balance[0]?.annual_leaves.reserved : '--' }} /
        {{ balance ? balance[0]?.annual_leaves.all : '--' }}
      </v-col>
      <v-col>
        {{ balance ? balance[0]?.emergency_leaves.reserved : '--' }} /
        {{ balance ? balance[0]?.emergency_leaves.all : '--' }}
      </v-col>
      <v-col>
        {{ balance ? balance[0]?.leave_excuses.reserved : '--' }} /
        {{ balance ? balance[0]?.leave_excuses.all : '--' }}
      </v-col>
    </v-row>
  </v-card>
</template>

<script lang="ts">
export default {
  name: 'vacationBalance',
  props: ['balance'],

  setup() {
    const vacationInfoHeaders = ['Annuals', 'Emergencies', 'Excuses']

    return {
      vacationInfoHeaders
    }
  }
}
</script>
<style scoped>
.v-card {
  box-shadow: none;
}
</style>
