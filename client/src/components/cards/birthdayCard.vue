<template>
  <v-card elevation="0" variant="outlined" color="white" class="pa-4 bg-balloons">
    <div class="d-flex flex-row-reverse">
      <v-icon class="me-2" @click.stop="$emit('close-dialog', false)"> mdi-close </v-icon>
    </div>
    <v-card-title class="text-center my-2 mb-5">
      <h3>
        <strong class="text-info">{{ firstname }}'s</strong>
        Birthday Today! 🎉🎂
      </h3>
      <!-- Wish a happy birthday to </h3> -->
    </v-card-title>

    <profileImage :with-link="true" v-show="birthday" :user="birthday" class="my-2" />

    <div class="w-100 text-center mt-6">
      Let's make sure to spread the birthday cheer and show {{ firstname }} how much
      {{ birthday.gender === 'Female' ? 'she' : 'he' }} means to us.
      <br />
      <strong class="text-warning">🎉🎂 Happy Birthday, {{ firstname }}!🎂🎉</strong>
    </div>

    <v-card elevation="0" variant="outlined" class="pa-4 mt-5">
      <v-row class="text-center">
        <v-col cols="6">
          <b>Name</b>
        </v-col>
        <v-col cols="6">
          {{ birthday.full_name }}
        </v-col>
      </v-row>
      <v-row class="text-center">
        <v-col cols="6">
          <b>Team</b>
        </v-col>
        <v-col cols="6">
          {{ birthday.team ? birthday.team : '--' }}
        </v-col>
      </v-row>
      <v-row class="text-center">
        <v-col cols="6">
          <b>Email</b>
        </v-col>
        <v-col cols="6">
          {{ birthday.email }}
        </v-col>
      </v-row>
    </v-card>
  </v-card>
</template>
<script lang="ts">
import profileImage from '@/components/profileImage.vue'

export default {
  name: 'birthdayCard',
  props: ['birthday'],
  emits: {
    'close-dialog': (item: Boolean) => item
  },

  components: {
    profileImage
  },

  setup(props) {
    const firstname = props.birthday.full_name.split(' ')[0]
    return {
      profileImage,
      firstname
    }
  }
}
</script>
