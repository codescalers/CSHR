<template>
  <v-container class="pa-6 mx-auto">
    <div class="my-6">
      <h2 class="font-weight-medium my-3">ThreeFold Team</h2>
      <v-divider></v-divider>
    </div>
    <officeFilters v-if="offices.state && offices.state.value" :offices="offices" :teams="teams" />
    <v-card class="pa-4" v-if="users.state.value.length">
      <v-row>
        <v-col class="d-flex flex-wrap justify-start">
          <v-col
            v-for="user of users.state.value"
            :key="user?.id"
            xl="3"
            lg="4"
            md="6"
            sm="12"
            cols="12"
            class=""
          >
            <div class="mt-1 text-center py-0 w-100">
              <router-link class="routerLink" :to="{ name: 'profile', query: { id: user.id } }">
                <UserCard :user="user" />
              </router-link>
            </div>
          </v-col>
        </v-col>
      </v-row>
      <v-pagination class="mt-4 mb-4" v-if="users.state.value.length" v-model="page" :length="count" rounded="circle"></v-pagination>
    </v-card>
    <v-card v-else class="pa-15 mt-15 d-flex justify-center text-center" variant="plain">
      Seems like there are no users. Please try changing the filters and attempting again.
    </v-card>
  </v-container>
</template>

<script lang="ts">
import type { Api } from '@/types'
import { ref, watch } from 'vue'
import { $api } from '@/clients'
import UserCard from '@/components/userCard.vue'
import officeFilters from '@/components/filters.vue'
import { useRoute } from 'vue-router'
import { useAsyncState } from '@vueuse/core'

export default {
  name: 'UsersView',
  components: {
    UserCard,
    officeFilters
  },
  setup() {
    const offices = useAsyncState($api.office.list(), [] as unknown as Api.Returns.List<Api.LocationType>, { immediate: true })
    const teams = [
      {name: 'Business Development'},
      {name: 'Development'},
      {name: 'HR & Finance'},
      {name: 'QA'},
      {name: 'Marketing and Communications'},
      {name: 'Operations'},
      {name: 'Support'}
    ]
    const $route = useRoute()
    const page = ref(1)
    const count = ref<number>(0)

    function setCount(data: any) {
      if (data?.count) {
        count.value = Math.ceil(data?.count / 12)
      } else {
        count.value = 0
      }
    }

    useAsyncState(
      $api.users.list({ team: $route.query.team, page: page.value }),
      undefined,
      {
        onSuccess(data) {
          setCount(data)
          users.execute(undefined, data?.results || [])
        }
      }
    )

    const users = useAsyncState(
      async (users: Api.User[]) => {
        return users
      },
      [],
      { immediate: false }
    )

    watch(
      () => [$route.query.location_id, $route.query.team_name, page.value],
      async () => {
        useAsyncState(
          $api.users.list({ location_id: $route.query.location_id, team_name: $route.query.team_name, page: page.value }),
          undefined,
          {
            onSuccess(data) {
              setCount(data)
              users.execute(undefined, data?.results || [])
            }
          }
        )
      }
    )

    return {
      users,
      page,
      count,
      offices,
      teams,
      UserCard,
      officeFilters
    }
  }
}
</script>

<style scoped>
.routerLink {
  text-decoration: none;
}
</style>
