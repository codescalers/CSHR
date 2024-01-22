<template>
  <v-card class="pa-5">
    <officeFilters :countries="countries" />

    <v-row>


      <v-col class="d-flex flex-wrap justify-center">
        <v-col v-for="user of users" :key="user?.id" xl="4" lg="6" md="12" sm="12" cols="12" class="px-5 py-5">
          <div class="mt-1 text-center py-0 w-100 ">
            <router-link class="routerLink" :to="{ name: 'profile', query: { id: user.id } }">
              <UserCard :user="user" />
            </router-link>


          </div>
        </v-col>
      </v-col>
    </v-row>
  </v-card>
</template>

<script lang="ts">
import type { Api, Country } from '@/types';
import { onMounted, ref, watch } from 'vue';
import { $api } from '@/clients';
import UserCard from "@/components/userCard.vue"
import officeFilters from '@/components/filters.vue';
import { useRoute } from 'vue-router';
export default {
  name: "UsersView",
  components: {
    UserCard,
    officeFilters,
  },
  setup() {
    const users = ref<Api.User[]>([]);
    const countriesSet = new Set<string>();
    const countries = ref<Country[]>([]);
    const countryMap = new Map<number, string>();

    const $route = useRoute()





    async function getUsers() {
      users.value = await $api.users.list({ "location_id": $route.query.location_id });
      for (const user of users.value) {
        countryMap.set(user.location.id, user.location.country);
        countriesSet.add(user.location.country)
      }
      countries.value = Array.from(countryMap).map(([id, country]) => ({
        id,
        country,
      }));
    }
    function setCountries() {
      for (const user of users.value) {
        countryMap.set(user.location.id, user.location.country);
        countriesSet.add(user.location.country)
      }
      countries.value = Array.from(countryMap).map(([id, country]) => ({
        id,
        country,
      }));
    }

    watch(
      () => $route.query.location_id,
      async newValue => {
        await getUsers();
      },
    );

    onMounted(async () => {
      await getUsers();
      setCountries();

    })

    return {
      users,
      UserCard,
      officeFilters,
      countries,

    }
  }
}
</script>

<style scoped>
.routerLink {
  text-decoration: none;
}
</style>