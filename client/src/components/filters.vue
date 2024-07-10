<template>
  <div>
    <v-row class="ma-1">
      <v-col cols="12" class="px-2">
        <v-alert color="warning">You can change the selected office to discover the team in other offices.</v-alert>
      </v-col>
    </v-row>
    <v-row class="mx-4">
      <v-col cols="6" sm="6" md="6" class="pa-1">
        <v-autocomplete clearable v-model="office" :items="offices.state.value" label="Office"
          @update:model-value="handleFiltersChange" return-object item-title="country">
        </v-autocomplete>
      </v-col>
      <v-col cols="6" sm="6" md="6" class="pa-1">
        <v-autocomplete clearable v-model="team" :items="teams" label="Team"
          @update:model-value="handleFiltersChange" return-object item-title="name" :disabled="office == undefined">
        </v-autocomplete>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import type { Api } from '@/types'

export default {
  name: 'officeFilters',
  props: ['offices', "teams"],

  setup(props) {
    const $router = useRouter()
    const office = ref<Api.Inputs.Office>()
    const team = ref()
    const $route = useRoute()


    const handleFiltersChange = () => {
      $router.push({ path: '/users', query: { location_id: office.value?.id, team_name: team.value?.name } })
    }

    watch(
      () => props.offices.state.value,
      async (_) => {
        if ($route.query.location_id && props.offices.state.value) {
          office.value = props.offices.state.value.find((office: any) => office.id === Number($route.query.location_id));
        }
      },
    );

    watch(
      () => props.teams,
      async (_) => {
        if ($route.query.team_name && props.teams) {
          team.value = props.teams.find((team: any) => team.name === $route.query.team_name);
        }
      },
    );
    return {
      office,
      team,
      handleFiltersChange,
    }
  }
}
</script>
