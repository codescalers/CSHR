<template>
  <v-card class="pa-5">
    <officeFilters :offices="offices" />

    <v-row>
      <v-col class="d-flex flex-wrap justify-center">
        <v-col v-for="user of users.state.value" :key="user?.id" xl="4" lg="6" md="12" sm="12" cols="12"
          class="px-5 py-5">
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
</template>

<script lang="ts">
import type { Api, Country } from '@/types'
import { onMounted, ref, watch } from 'vue'
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
    const offices = useAsyncState($api.office.list(), [], { immediate: true })
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
                  count.value = Math.ceil(data?.count / 10)
              } else {
                count.value = 0
              }
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
      () => $route.query.location_id,
      async (newValue) => {
        page.value = 1
        useAsyncState(
          $api.users.list({ location_id: $route.query.location_id, page: page.value }),
          undefined,
          {
            onSuccess(data) {
              if (data?.count) {
                  count.value = Math.ceil(data?.count / 10)
              } else {
                count.value = 0
              }
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
              if (data?.count) {
                  count.value = Math.ceil(data?.count / 10)
              } else {
                count.value = 0
              }
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
