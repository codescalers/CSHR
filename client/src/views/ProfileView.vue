<template>
  <div>
    <v-row class="ma-5">
      <v-col cols="12" sm="12" md="3" class="pa-2 rounded ma-2 align-self-start">
        <UserCard :loading="user.isLoading" :user="user.state.value" />
      </v-col>
      <v-col cols="12" sm="12" md="8" class="pa-2 border rounded position-relative ma-2">
        <div>
          <personalInformation :user="user.state.value" />
          <!-- v-if="showBalance" -->
          <vacationBalance :balance="balance.state.value" />
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent } from 'vue'
import vacationBalance from '@/components/vacationBalance.vue'
import personalInformation from '@/components/personalInformation.vue'
import { $api } from '@/clients'
import { useRoute } from 'vue-router'
import { useAsyncState } from '@vueuse/core'
import profileImage from '@/components/profileImage.vue'
import UserCard from '@/components/userCard.vue'
import { ApiClientBase } from '@/clients/api/base'

export default defineComponent({
  components: {
    vacationBalance,
    personalInformation,
    UserCard
  },

  setup() {
    const $route = useRoute()
    const storedUser = ApiClientBase.user
    const user = useAsyncState(
      $route.query.id ? $api.users.getuser(Number($route.query.id)) : $api.myprofile.getUser(),
      [],
      {
        onSuccess(data) {
          balance.execute(undefined, data.id)
        }
      }
    )

    const balance = useAsyncState(
      async (id: number) => {
        return $api.vacations.getVacationBalance({ user_ids: id })
      },
      null,
      { immediate: false }
    )

    // const showBalance = computed(() => {
    //   if (storedUser.value?.fullUser) {
    //     if (
    //       user.state.value &&
    //       storedUser.value?.fullUser &&
    //       user.state.value.id === storedUser.value?.fullUser.id
    //     ) {
    //       return true
    //     } else if (storedUser.value?.fullUser && storedUser.value?.fullUser.user_type === 'Admin') {
    //       if (user.state.value.reporting_to) {
    //         if (
    //           user.state.value.reporting_to.includes(storedUser.value?.fullUser.id) &&
    //           user.state.value.location.name === storedUser.value?.fullUser.location.name
    //         ) {
    //           return true
    //         }
    //       }
    //       return false
    //     }
    //   }
    //   return false
    // })

    return {
      user,
      balance,
      // showBalance,
      vacationBalance,
      personalInformation,
      profileImage
    }
  }
})
</script>
