<template>
  <router-link v-if="withLink" :to="`/profile?id=${user.id}`" style="text-decoration: none">
    <div v-if="user.image?.includes('profile_image')" class="d-flex justify-center">
      <img
        :src="imageSrc + user.image"
        class="user-profile-image rounded-circle"
        :style="{ width: width || '70px', height: width || '70px', objectFit: 'cover' }"
      />
    </div>

    <div v-else>
      <v-avatar :color="user.image" size="40" class="d-flex mx-auto user-profile-logo">
        <span class="text-h6 text-uppercase">{{ avatar }}</span>
      </v-avatar>
    </div>
  </router-link>

  <div v-else>
    <div v-if="user.image?.includes('profile_image')" class="d-flex justify-center">
      <img
        :src="imageSrc + user.image"
        class="user-profile-image rounded-circle"
        :style="{ width: width || '70px', height: width || '70px', objectFit: 'cover' }"
      />
    </div>

    <div v-else>
      <v-avatar :color="user.image" size="50" class="d-flex mx-auto user-profile-logo">
        <span class="text-h5 text-uppercase">{{ avatar }}</span>
      </v-avatar>
    </div>
  </div>
</template>

<script lang="ts">
import { computed } from 'vue'

export default {
  name: 'profileImage',
  props: ['user', 'withLink', 'width'],

  setup(props) {
    const imageSrc = window.env.SERVER_DOMAIN_NAME_API.replace('api', '')
    const avatar = computed(() => {
      if (props.user.full_name) {
        let val = String(props.user.full_name)
        return val.charAt(0)
      }
      return props.user.email?.charAt(0) + props.user.email?.charAt(1)
    })

    return {
      avatar,
      imageSrc
    }
  }
}
</script>

<style scoped>
.user-profile-logo {
  cursor: pointer;
}
</style>
