<template>
  <v-card color="title" class="py-10 hover-card border bg-graytitle">
    <div
      v-if="loading === true"
      class="d-flex align-center justify-center items-center py-0 font-weight-bold"
    >
      <v-progress-circular color="primary" indeterminate :size="47"></v-progress-circular>
    </div>
    <div v-else>
      <div class="d-flex align-center justify-center items-center py-0 font-weight-bold">
        <profileImage v-show="user" :user="user" />
      </div>
      <div v-if="user && user.email && user.email.length && !user.is_active" class="inactive">
        Inactive User
      </div>
      <v-card-title class="text-center"> {{ user.full_name }}</v-card-title>
      <v-card-text class="card-body light pt-0 pb-1 text-center text-subtitle-2">
        {{ user.job_title }} / {{ user.team }}
      </v-card-text>
      <v-card-text class="card-body text-center light pt-0 pb-1 text-subtitle-2">
        {{ user.email }}
      </v-card-text>
      <v-card-text
        v-if="user.location"
        class="card-body text-center light pt-0 pb-1"
        style="font-size: 0.875rem"
      >
        {{ user.location.name }}
      </v-card-text>
    </div>
  </v-card>
</template>

<script lang="ts">
import profileImage from './profileImage.vue'

export default {
  name: 'UserCard',
  props: ['user', 'loading'],
  components: {
    profileImage
  },

  setup() {
    return {
      profileImage
    }
  }
}
</script>

<style scoped>
.hover-card:hover {
  transform: scale(1.01);
  /* Increase the scale on hover */
  transition: transform 0.3s ease;
  /* Add a smooth transition effect */
}
.inactive {
  position: absolute;
  top: 21px;
  left: -40px;
  transform: rotate(-35deg);
  background: brown;
  padding: 4px;
  width: 187px;
  text-align: center;
  margin: 0 auto;
  justify-content: center;
  align-items: center;
  font-weight: 400;
  color: white;
}
</style>
