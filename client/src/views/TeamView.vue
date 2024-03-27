<template>
  <v-container class="pa-6 mx-auto">
    <div v-if="supervisors && supervisors.length > 0">
      <div class="my-6">
        <h2 class="font-weight-medium my-6">Team Lead</h2>

        <v-divider></v-divider>
      </div>
      <v-row>

        <v-col v-for="(person, index) in supervisors" :key="index" cols="12">
          <v-card class="elevation-4 my-4 pa-3 border bg-graytitle">
            <v-img v-if="person.image.startsWith('/media')" :src="person.image" height="200"
              class="grey lighten-2"></v-img>
            <v-card-title class="text-h6 ml-4 font-weight-bold">{{
              person.full_name
            }}</v-card-title>
            <v-card-subtitle class="text-body-1 ml-4">{{ person.job_title }}</v-card-subtitle>
            <v-card-text class="py-1">
              <v-list dense class="d-flex bg-graytitle">
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title class="text-body-2">Email: {{ person.email }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title class="text-body-2">Team: {{ person.team }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title class="text-body-2">Mobile Number: {{ person.mobile_number }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>
    <div class="my-6">
      <h2 class="font-weight-medium my-6">My Team</h2>
      <v-divider></v-divider>
    </div>

    <v-data-table :headers="headers" :loading="loading" :items="team" class="mb-6">
      <template v-slot:loading>
        <v-skeleton-loader type="table-row@5"></v-skeleton-loader>
      </template>
      <template v-slot:item="{ item }">
        <tr>
          <td v-for="(header, index) in headers" :key="index">
            {{ displayValue((item as any)[header.key]) }}
          </td>
        </tr>
      </template>
    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import { $api } from '@/clients'
import {  watch } from 'vue'
import { onMounted, ref } from 'vue'

export default {
  name: 'TeamView',
  setup() {
    const headers = [
      { title: 'Name', sortable: false, key: 'full_name' },
      { title: 'Email', key: 'email' },
      { title: 'Phone', key: 'mobile_number' },
      { title: 'Position', key: 'job_title' },
      { title: 'Telegram', key: 'telegram_link' },
      { title: 'Department', key: 'team' }
    ] as any[]
    const loading = ref(true)
    const supervisors = ref()
    const page = ref(1)
    const count = ref<number>(0)
    const team = ref<any[]>([]);


    function displayValue(value: any) {
      return value ?? '-'
    }

    async function listTeam(page: number, count: number): Promise<{ page: number, count: number, team: any[] }> {

      const res = await $api.users.team.list({ page });
      let team: any[] = [];
      if (res.count) {
        count = Math.ceil(res.count / 10)
      } else {
        count = 0
      }
      res.results.forEach((user: any) => {
        team.push(user)
      })
      return { page, count, team };

    }

    async function concatTeam() {
      const { page: currentPage, count: currentCount, team: teamUsers } = await listTeam(page.value, count.value);
      page.value = currentPage + 1;
      count.value = currentCount - 1;
      team.value = team.value.concat(teamUsers);
    }
    watch(
      () => count.value,
      async (newValue) => {
        if (page.value !== count.value && count.value >= 1) {
          concatTeam();
        }
      })

    onMounted(async () => {
      try {
        supervisors.value = await $api.users.team.supervisors.list()
        concatTeam()
        loading.value = false
      } catch (error) {
        console.error(error)
      }
    })

    return {
      headers,
      loading,
      team,
      supervisors,
      displayValue
    }
  }
}
</script>
