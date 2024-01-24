<template>
  <div>
    <v-card class="ma-5 pa-2 border rounded ma-2 align-self-start">
      <v-row class="ma-5">
        <v-col cols="12" class="py-5 px-2">
          <v-alert color="warning">You can change the selected office to discover the team in other offices.</v-alert>
        </v-col>
      </v-row>
      <v-row class="ma-5">
        <v-col cols="12" sm="12" md="2" class="px-2 align-self-start">

          <div>
            <h3> Select Office</h3>
          </div>
        </v-col>
        <v-col cols="12" sm="12" md="10" class="pa-2 align-self-start">
          <div>



            <v-autocomplete v-model="office" :items="offices" label="Office" @update:model-value="handleOfficeChange"
              return-object item-title="country">
            </v-autocomplete>

          </div>

        </v-col>
      </v-row>
    </v-card>

  </div>
</template>

<script lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router'

import type { Country } from '@/types';


export default {
  name: 'officeFilters',
  props: ["offices"],

  setup(props) {
    const $router = useRouter()
    const office = ref<Country>();

    const handleOfficeChange = () => {
      $router.push({ path: '/users', query: { location_id: office.value?.id } });
    };
    return {
      office,
      handleOfficeChange,

    }
  }
}
</script>

