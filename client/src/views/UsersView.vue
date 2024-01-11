<template>
  <v-card class="pa-5">
    <officeFilters :countriesSet="countriesSet" />

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
import type { Api } from '@/types';
import { onMounted, ref } from 'vue';
import { $api } from '@/clients';
import UserCard from "@/components/userCard.vue"
import officeFilters from '@/components/filters.vue';
export default {
  name: "UsersView",
  components: {
    UserCard,
    officeFilters,
  },
  setup() {
    const users = ref<Api.User[]>([]);


    // const countries = ref<string[]>([]);
    const countriesSet = ref<Set<string>>(new Set());
    // user.location.country

    async function getUsers() {
      users.value = await $api.users.list();
      for (const user of users.value) {
        countriesSet.value.add(user.location.country)
        // console.log("countries.value ",countriesSet.value)
      }

    }

    async function login(email: string, password: string) {
      await $api.auth.login({
        email,
        password
      });
    }
    onMounted(async () => {
      await login("admin@gmail.com", "0000");
      await getUsers();

    })

    return {
      users,
      UserCard,
      officeFilters,
      countriesSet,

    }
  }
}
</script>

<style scoped>
.routerLink{
     text-decoration: none;
 }
 
</style>