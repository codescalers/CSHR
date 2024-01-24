<template>
  <div v-if="user.image?.includes('profile_image')" class="d-flex justify-center mb-5">
    <img :src="imageSrc + user.image" class="user-profile-image rounded-circle"
      style="width:70px; height:70px;" />
  </div>

  <div v-else>
    <v-avatar :color="user.image" size="50" class="d-flex mx-auto mt-5 mb-3">
      <span class="text-h5 text-uppercase">{{ avatar }}</span>
    </v-avatar>
  </div>
</template>

<script lang="ts">
import { computed } from 'vue';


export default {
  name: 'profileImage',
  props: ["user"],

  setup(props) {
    const imageSrc = window.env.SERVER_DOMAIN_NAME_API.replace("api", "")
    const avatar = computed(() => {
      if (props.user.full_name) {
        let val = String(props.user.full_name);
        return val.charAt(0);
      }
      return props.user.email?.charAt(0) + props.user.email?.charAt(1);
    });


    return {
      avatar,
      imageSrc,
    }
  }
}
</script>

