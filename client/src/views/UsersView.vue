<template>
  <v-container class="pa-6 mx-auto">
    <div class="my-6">
      <h2 class="font-weight-medium my-3">ThreeFold Team</h2>
      <v-divider></v-divider>
    </div>
    <officeFilters :offices="offices" />
    <v-card class="pa-2">
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
      <v-row>
        <v-col class="d-flex flex-wrap justify-center">
          <v-pagination v-model="page" :length="count" rounded="circle"></v-pagination>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import type { Api, Country } from '@/types'
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
    const offices = ref<Country[]>([])
    const $route = useRoute()
    let isFirstLoad = true
    const page = ref(1)
    const count = ref<number>(0)

    useAsyncState(
      $api.users.list({ location_id: $route.query.location_id, page: page.value }),
      undefined,
      {
        onSuccess(data) {
          if (data?.count) {
            count.value = data.count / 10
            count.value = Math.ceil(data.count / 10)
          }
          users.execute(undefined, data?.results || [])
        }
      }
    )

    const users = useAsyncState(
      async (users: Api.User[]) => {
        if (isFirstLoad) {
          offices.value = Array.from(new Set(users.map((user) => user.location.id))).map((id) => {
            const user = users.find((u) => u.location.id === id)
            return { id: user?.location.id ?? 0, country: user?.location.country ?? '' }
          })
        }

        isFirstLoad = false
        return users
      },
      [],
      { immediate: false }
    )

    watch(
      () => $route.query.location_id,
      async (newValue) => {
        page.value = 1
        useAsyncState(
          $api.users.list({ location_id: $route.query.location_id, page: page.value }),
          undefined,
          {
            onSuccess(data) {
              users.execute(undefined, data?.results || [])
            }
          }
        )
      }
    )

    watch(
      () => page.value,
      async (newValue) => {
        useAsyncState(
          $api.users.list({ location_id: $route.query.location_id, page: page.value }),
          undefined,
          {
            onSuccess(data) {
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
