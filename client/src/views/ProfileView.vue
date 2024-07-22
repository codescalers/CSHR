<template>
  <div>
    <v-row class="ma-5">
      <v-col cols="12" sm="12" md="12" lg="3" class="pa-2 rounded ma-2 align-self-start">
        <v-card-title class="font-weight-medium bg-primary">User info</v-card-title>
        <UserCard :loading="user.isLoading" :user="user.state.value" />
        <div v-if="user.state.value.reporting_to && user.state.value.reporting_to.length">
          <v-divider class="mt-4 mb-4"></v-divider>
          <v-card-title class="font-weight-medium bg-primary">Team lead</v-card-title>
          <UserCard :loading="user.isLoading" :user="user.state.value.reporting_to[0]" />
        </div>
      </v-col>
      <v-col cols="12" sm="12" md="12" lg="8" class="pa-2 border rounded position-relative ma-2">
        <div>
          <personalInformation :user="user.state.value" />
          <vacationBalance :balance="balance.state.value" v-if="couldSeeBalance" />
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

    const couldSeeBalance = computed(() => {
      return user.state.value.leads && user.state.value.leads.includes(requestedUser!.id) || requestedUser!.id === user.state.value.id
    })

    const balance = useAsyncState(
      async (id: number) => {
        return $api.vacations.getVacationBalance({ user_ids: id })
      },
      null,
      { immediate: false }
    )

    return {
      user,
      balance,
      couldSeeBalance,
      vacationBalance,
      personalInformation,
      profileImage
    }
  }
})
</script>
