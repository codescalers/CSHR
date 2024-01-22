<template>
  <v-card class="pa-4">
    <div class="d-flex my-2">
      <v-card-title class="font-weight-bold mb-3"> {{ $props.title }} </v-card-title>
  
      <v-card-subtitle class="mt-2">
        <v-chip :color="getStatusColor($props.status)">
          {{ $props.status }}
        </v-chip>
      </v-card-subtitle>
    </div>

    <v-row no-gutters class="mx-3">
      <v-col v-for="section in sections" :key="section.key" cols="12">
        <v-card class="mb-6 elevation-12">
          <v-card-title class="card-title bg-primary white--text">{{ section.title }}</v-card-title>

          <v-list class="custom-list">
            <v-row v-for="detail in section.details" :key="detail.label" class="ma-1 bordered" no-gutters>
              <v-col cols="3">
                <v-list-item>
                  <v-list-item-content class="ma-0">
                    {{ detail.label }}
                  </v-list-item-content>
                </v-list-item>
              </v-col>

              <v-col cols="9">
                <v-list-item>
                  <v-list-item-content>
                    {{ detail.value }}
                  </v-list-item-content>
                </v-list-item>
              </v-col>
            </v-row>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
    <v-card-actions>
      <v-btn color="primary" @click="closeDialog()">Close</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { computed, type PropType } from 'vue'
import { getStatusColor } from '@/utils'

export default {
  name: 'NotificationDetails',
  props: {
    eventId: {
      type: Number,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    status: {
      type: String,
      required: true
    },
    sections: {
      type: Array as PropType<any[]>,
      required: true
    },
    onClose: {
      type: Function as PropType<() => void>,
      required: true
    }
  },
  setup(props) {
    const color = computed(() => getStatusColor(props.status))

    const closeDialog = () => {
      props.onClose()
    }

    return {
      color,
      closeDialog,
      getStatusColor
    }
  }
}
</script>

<style scoped>
.card-title{
  font-size: 1rem !important;
  line-height: 1.5rem !important;
}
</style>
