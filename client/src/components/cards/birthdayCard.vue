<template>
  <v-card elevation="0" class="bg-balloons">
    <v-card-title class="bg-graytitle">
    <div class="d-flex flex-row-reverse">
      <v-icon size="small" class="me-2" @click.stop="$emit('close-dialog', false)"> mdi-close </v-icon>
    </div>
  </v-card-title>
  <v-container class="pa-4">
    <div class="mt-3">
    <profileImage :with-link="true" v-show="birthday" :user="birthday" class="my-4" />
      <h4 class="text-center my-3">
        <strong class="text-info">{{ firstname }}'s</strong>
        Birthday Today! 🎉🎂
      </h4>
      <!-- Wish a happy birthday to </h3> -->
    </div>
    <div class="text-subtitle-2 text-center font-weight-regular mt-2">
      Let's make sure to spread the birthday cheer and show {{ firstname }} how much
      {{ birthday.gender === 'Female' ? 'she' : 'he' }} means to us.
      <br />
      <strong class="text-warning text-subtitle-1">🎉🎂 Happy Birthday, {{ firstname }}!🎂🎉</strong>
    </div>

    <v-divider class="my-2"></v-divider>

    <v-card elevation="0" class="pa-4 mt-5">
      <v-row class="text-center text-subtitle-2 d-flex justify-center">
        <v-col cols="4" class="d-flex">
          <b>Name :</b>
          <span class="mx-2 font-weight-regular">{{ birthday.full_name }}</span>
        </v-col>
        <v-col cols="4">
          <b>Team :</b>
          <span class="mx-2 font-weight-regular">{{ birthday.team ? birthday.team : '--' }}</span>
        </v-col>
        <v-col cols="4">
          <b>Email :</b>
          <span class="mx-2 font-weight-regular">{{ birthday.email }}</span>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
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
