<template>
  <v-card class="pa-4">
    <v-card-title class="font-weight-bold mb-3"> {{ $props.title }} </v-card-title>

    <v-card-subtitle>
      <v-chip :color="getStatusColor($props.status)">
        {{ $props.status }}
      </v-chip>
    </v-card-subtitle>

    <v-row class="mt-4">
      <v-col v-for="section in sections" :key="section.title" cols="12" md="6">
        <v-list dense>
          <v-list-item-group>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title class="mb-3 font-weight-bold">
                  {{ section.title }}
                </v-list-item-title>
                <v-list-item-subtitle v-for="detail in section.details" :key="detail.label">
                  {{ detail.label }}: {{ detail.value }}
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-col>
    </v-row>

    <v-card-actions class="mt-6">
      <v-btn color="blue darken-1" @click="closeDialog()"> Close </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'

export default defineComponent({
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
    const getStatusColor = (status: string) => {
      switch (status) {
        case 'approved':
          return 'green'
        case 'pending':
          return 'orange'
        case 'rejected':
          return 'red'
        default:
          return 'grey'
      }
    }

    const closeDialog = () => {
      props.onClose()
    }

    return {
      closeDialog,
      getStatusColor
    }
  }
})
</script>
