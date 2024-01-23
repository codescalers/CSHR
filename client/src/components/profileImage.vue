<template>
  <div v-if="image?.includes('profile_image')">
    <img :src="imageSrc + image" class="user-profile-image rounded-circle" style="width:{size}px; height:{size}px;"
 />
  </div>

  <div v-esle>
    <v-avatar :color="image" size="50" class="d-flex mx-auto mt-5 mb-3">
      <span class="text-h5 text-uppercase">{{ fullName? avatar : "??" }}</span>
    </v-avatar>
  </div>
</template>

<script lang="ts">
import { computed } from 'vue';


export default {
  name: 'profileImage',
  props: ["image", "fullName"],

  setup(props) {
    const imageSrc = window.env.CSHR_API
    const avatar = computed(() => {
      if (props.fullName) {
        let val = String(props.fullName);
        return val.charAt(0);
      }
      return "??";
    });


    return {
      avatar,
      imageSrc,
    }
  }
}
</script>

