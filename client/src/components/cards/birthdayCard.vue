<template>
  <v-card elevation="0" variant="outlined" color="white" class="pa-4">
    <div class="d-flex flex-row-reverse">
      <v-icon class="me-2" @click.stop="$emit('close-dialog', false)"> mdi-close </v-icon>
    </div>
    <v-card-title class="text-center my-2">
      <h1>Wish a happy birthday to</h1>
    </v-card-title>

    <profileImage v-show="birthday" :user="birthday"  class=" my-2"/>

    <v-card elevation="0" variant="outlined" class="pa-4 mt-2">
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
          {{ birthday.team ? birthday.team : "--" }}
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
import profileImage from "@/components/profileImage.vue";


export default {
  name: "birthdayCard",
  props: ["birthday"],
  emits: {
    'close-dialog': (item: Boolean) => item
  },

  components: {
    profileImage,
  },

  setup(props) {
    return {

      profileImage,
    };
  },
};
</script>
