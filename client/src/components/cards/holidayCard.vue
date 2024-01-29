<template>
  <v-card elevation="0" variant="outlined" color="white" class="pa-4">
    <div class="d-flex flex-row-reverse">
      <v-icon class="me-2" @click.stop="$emit('close-dialog', false)"> mdi-close </v-icon>
    </div>
    <div class="d-flex expired" v-if="holiday.expired">expired</div>
    <v-card-title class="text-center mb-5 my-2">
      <h1 :class="`${holiday.expired ? 'text-error' : ''}`">{{ holiday.location.country }}</h1>
    </v-card-title>
    <hr class="mb-2" />
    <v-card elevation="0" variant="outlined" class="pa-4 mt-2">
      <v-row class="pa-2">
        <p class="pa-5">
          <b>{{ holiday.holiday_date }}</b> is a public holiday in
          <b>{{ holiday.location.country }}</b
          >, We hope you and your family have a peaceful and enjoyable holiday. Please be aware that
          our office in <b>{{ holiday.location.country }}</b
          >, will be closed on this date. Thank you!
        </p>
      </v-row>
    </v-card>
  </v-card>
</template>
<script lang="ts">
export default {
  name: 'holidayCard',
  props: ['holiday'],
  emits: {
    'close-dialog': (item: Boolean) => item
  }
}
</script>

<style scoped>
.expired {
  position: absolute;
  top: 15px;
  left: -32px;
  transform: rotate(-35deg);
  background: brown;
  padding: 4px;
  width: 142px;
  text-align: center;
  margin: 0 auto;
  justify-content: center;
  align-items: center;
  font-weight: 700;
  color: white;
}
</style>
