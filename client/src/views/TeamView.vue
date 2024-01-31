<template>
  <v-container class="pa-6 mx-auto">
    <div v-if="supervisors && supervisors.length > 0">
      <div class="my-6">
        <h3 class="font-weight-medium my-6">Team Lead</h3>
        <v-divider></v-divider>
      </div>
      <v-row>
        <v-col v-for="(person, index) in supervisors" :key="index" cols="12" md="6" lg="6">
          <v-card class="elevation-4 my-4">
            <v-img
              v-if="person.image.startsWith('/media')"
              :src="person.image"
              height="200"
              class="grey lighten-2"
            ></v-img>
            <v-card-title class="text-h6 font-weight-bold">{{ person.full_name }}</v-card-title>
            <v-card-subtitle class="text-body-1">{{ person.job_title }}</v-card-subtitle>
            <v-card-text>
              <v-list dense>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title class="text-body-2"
                      >Email: {{ person.email }}</v-list-item-title
                    >
                  </v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title class="text-body-2"
                      >Team: {{ person.team }}</v-list-item-title
                    >
                  </v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title class="text-body-2"
                      >Mobile Number: {{ person.mobile_number }}</v-list-item-title
                    >
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
import { onMounted, ref } from 'vue'

export default {
  name: 'TeamView',
  setup() {
    const headers = [
      { title: 'Name', sortable: false, key: 'full_name' },
      { title: 'Email', key: 'email' },
      { title: 'Phone', key: 'phone' },
      { title: 'Position', key: 'position' },
      { title: 'Telegram', key: 'telegram_link' },
      { title: 'Department', key: 'team' }
    ] as any[]
    const loading = ref(true)
    const team = ref()
    const supervisors = ref()

    function displayValue(value: any) {
      return value ?? '-'
    }

    onMounted(async () => {
      try {
        team.value = await $api.users.team.list()
        supervisors.value = await $api.users.team.supervisors.list()
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
