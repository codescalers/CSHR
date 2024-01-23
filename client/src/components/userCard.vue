<template>
  <v-card color="title" class="py-10 ma-5 hover-card">
    <div class="d-flex align-center justify-center items-center py-0 font-weight-bold">
      <profileImage  v-show="user" :image="user?.image" :fullName="user?.full_name"/>

    </div>
    <div class="my-3">
      <v-card-title> {{ user.full_name }}</v-card-title>


      <v-card-text class="card-body light pt-0 pb-1" style="font-size: 0.875rem"> {{ user.job_title }} / {{
        user.team }} </v-card-text>
      <v-card-text class="card-body light pt-0 pb-1" style="font-size: 0.875rem"> {{ user.email }} </v-card-text>
      <v-card-text class="card-body light pt-0 pb-1" style="font-size: 0.875rem">
        {{ user.location.country }}</v-card-text>

    </div>

  </v-card>
</template>

<script lang="ts">
import profileImage from "./profileImage.vue";

export default {
  name: 'UserCard',
  props: ["user"],
  components: {
    profileImage,
  },
  setup(props) {

    return {
      profileImage,
    }
  }
}
</script>

<style scoped>
.hover-card:hover {
  transform: scale(1.05); /* Increase the scale on hover */
  transition: transform 0.3s ease; /* Add a smooth transition effect */
}
</style>