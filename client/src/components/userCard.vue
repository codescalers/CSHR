<template>
  <v-card color="title">
    <div class="d-flex align-center justify-center items-center py-0 font-weight-bold">
      <v-avatar color="primary" size="50" class="d-flex mx-auto mt-5 mb-3">
        <span class="text-h5 text-uppercase">{{ user?.image ? avatar(user.full_name) : "?" }}</span>
      </v-avatar>

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

export default {
  name: 'UserCard',
  props: ["user"],

  setup(props) {
    function avatar(name: string) {
      if (name) {
        let val = String(name);
        return val.charAt(0);
      }
      return "??";
    }

    return {
      avatar,
    }
  }
}
</script>

