<template>
  <v-card elevation="0">
    <v-card-title class="bg-graytitle">
      <div class="d-flex flex-row-reverse">
        <v-icon size="small" class="me-2" @click.stop="$emit('close-dialog', false)">
          mdi-close
        </v-icon>
      </div>
    </v-card-title>
    <v-container class="pa-4">
      <v-card elevation="0" class="mt-2">
        <v-row class="pa-2 text-center">
          <p class="pa-5">
            <b>{{ holiday.holiday_date }}</b> is a public holiday in
            <b class="text-error">{{ holiday.location.country }}</b
            >, We hope you and your familys have a peaceful and enjoyable holiday. Please be aware
            that our office in <b class="text-error">{{ holiday.location.country }}</b
            >, will be closed on this date. Thank you!
          </p>
        </v-row>
      </v-card>
    </v-container>
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
  top: 14px;
  left: -40px;
  transform: rotate(-35deg);
  background: brown;
  padding: 3px;
  width: 142px;
  text-align: center;
  margin: 0 auto;
  justify-content: center;
  align-items: center;
  font-weight: 400;
  color: rgb(255, 255, 255);
}
</style>
