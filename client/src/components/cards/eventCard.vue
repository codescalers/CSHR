<template>
  <v-card elevation="0">
    <v-card-title class="bg-graytitle">
    <div class="d-flex flex-row-reverse">
      <v-icon size="small" class="me-2" @click.stop="$emit('close-dialog', false)"> mdi-close </v-icon>
    </div>
  </v-card-title>
  <v-container class="pa-4">
    <v-card-title class="text-center my-2">
      <b>{{ event.name }}</b>
      <v-divider class="my-2"></v-divider>
    </v-card-title>
    <div elevation="1" variant="text" class="pa-4 mb-3">    
        <h4>Description</h4>
      <p class="text-subtitle-2 font-weight-regular mt-2">
        {{ event.description ? event.description : '--' }}
      </p>
    </div>
    <!-- <v-card elevation="0" variant="outlined" color="white" class="px-4"> -->
    <v-row class="text-center mx-2 mt-2">
      <v-col cols="6" class="mt-2 border" v-for="header in headers" :key="header">
        <strong>{{ header }}</strong>
      </v-col>
    </v-row>

    <v-row class="text-center mx-2 mb-2">
      <v-col cols="6" class="border">
        {{ fromDateTime }}
      </v-col>

      <v-col cols="6" class="border">
        {{ toDateTime }}
      </v-col>

      
    </v-row>
  </v-container>

    <!-- </v-card> -->
  </v-card>
</template>
<script lang="ts">
import { ref } from 'vue'
import { formatDateTime } from '@/utils'

export default {
  name: 'eventCard',
  props: ['event'],
  emits: {
    'close-dialog': (item: Boolean) => item
  },

  setup(props) {
    const fromDateTime = formatDateTime(props.event.from_date)
    const toDateTime = formatDateTime(props.event.end_date)
    const headers = ref(['From', 'To'])

    return {
      fromDateTime,
      toDateTime,
      headers
    }
  }
}
</script>
