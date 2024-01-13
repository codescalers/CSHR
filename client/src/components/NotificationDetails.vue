<template>
  <v-card>
    <v-card-title class="font-weight-bold mb-3">
      {{ details.title || capitalize(details.reason.split('_').join(' ')) }}
    </v-card-title>

    <v-card-subtitle>
      <v-chip :color="getStatusColor(details.status)">
        {{ details.status }}
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
                <v-list-item-subtitle v-for="subtitle in section.subtitles" :key="subtitle.label">
                  {{ subtitle.label }}: {{ subtitle.value }}
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-col>
    </v-row>

    <v-card-actions class="mt-6">
      <v-btn color="blue darken-1" @click="closeDialog"> Close </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { defineComponent, type PropType, ref } from 'vue';
import { capitalize } from 'vue';

export default defineComponent({
  name: 'NotificationDetails',
  props: {
    details: {
      type: Object as PropType<any>,
      required: true,
    },
    sections: {
      type: Array as PropType<any[]>,
      required: true,
    },
    onClose: {
      type: Function as PropType<() => void>,
      required: true,
    },
  },
  setup(props) {
    const getStatusColor = (status: string) => {
      switch (status) {
        case 'approved':
          return 'green';
        case 'pending':
          return 'orange';
        case 'rejected':
          return 'red';
        default:
          return 'grey';
      }
    };

    const closeDialog = () => {
      props.onClose();
    };

    return {
      closeDialog,
      getStatusColor,
      capitalize,
    };
  },
});
</script>
