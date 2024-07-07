<template>
  <div>
    <v-row class="ma-5">
      <v-col cols="12" sm="12" md="3" class="pa-2 rounded ma-2 align-self-start">
        <v-alert class="mb-4" color="primary" variant="outlined">User info</v-alert>
        <UserCard :loading="user.isLoading" :user="user.state.value" />
        <div v-if="couldSeeReportingTo">
          <v-divider class="mt-4 mb-4"></v-divider>
          <v-alert class="mb-4" color="primary" variant="outlined">Reporting to</v-alert>
          <UserCard :loading="user.isLoading" :user="user.state.value.reporting_to[0]" />
        </div>
      </v-col>
      <v-col cols="12" sm="12" md="8" class="pa-2 border rounded position-relative ma-2">
        <div>
          <personalInformation :user="user.state.value" />
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
import type { Api } from '@/types'

export default defineComponent({
  components: {
    vacationBalance,
    personalInformation,
    UserCard
  },

  setup() {
    const $route = useRoute()
    const requestedUser = ApiClientBase.user.value?.fullUser

    const user = useAsyncState<Api.User>(
      $route.query.id ? $api.users.getuser(Number($route.query.id)) : $api.myprofile.getUser(),
      {} as unknown as Api.User,
      {
        onSuccess(data) {
          balance.execute(undefined, data.id)
        }
      }
    )

    const couldSeeReportingTo = computed(() => {
      return (
        user.state.value.reporting_to && user.state.value.reporting_to.length &&
        ((requestedUser && user.state.value.id === requestedUser.id) ||
          (requestedUser && requestedUser.user_type === 'Admin'))
      )
    })

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
      couldSeeReportingTo,
      // showBalance,
      vacationBalance,
      personalInformation,
      profileImage
    }
  }
})
</script>
