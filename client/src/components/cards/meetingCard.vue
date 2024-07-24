<template>
  <v-card elevation="0">
    <v-card-title class="bg-graytitle">
      <div class="d-flex flex-row-reverse">
        <v-icon size="small" class="me-2" @click.stop="$emit('close-dialog', false)">
          mdi-close
        </v-icon>
      </div>
    </v-card-title>
    <v-container class="pa-6">
      <v-card-title class="text-center my-2">
        Meeting Created by
        <b>{{ meeting.host_user.full_name }}</b>
      </v-card-title>
      <v-divider class="my-2"></v-divider>
      <v-card elevation="0" variant="text" class="pa-4 mb-0"> </v-card>
      <v-row class="text-center mx-2 mb-2">
        <v-col cols="6" class="border">
          <b>Team</b>
          <span class="mx-2">{{ meeting.host_user.team ? meeting.host_user.team : '--' }}</span>
        </v-col>
        <v-col cols="6" class="border">
          <b>Meeting Link :</b>
          <a :href="meeting.meeting_link" target="_blank"
            ><v-icon class="mx-2"> mdi-link </v-icon>Meeting Link</a
          >
        </v-col>
        <v-col cols="12" class="border">
          Date :<span class="mx-2">{{ formatedDateTime }}</span>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>
<script lang="ts">
import { formatDateTime } from '@/utils'

export default {
  name: 'meetingCard',
  props: ['meeting'],
  emits: {
    'close-dialog': (item: Boolean) => item
  },

  setup(props) {
    const formatedDateTime = formatDateTime(props.meeting.date)

    return {
      formatedDateTime,
    }
  }
}
</script>
