<template>
  <div>
<v-row class="ma-1">
      <v-col cols="12" class="px-2">
        <v-alert color="warning"
          >You can change the selected office to discover the team in other offices.</v-alert
        >
      </v-col>
    </v-row>
    <v-row class="ma-2">
      <v-col cols="12" sm="12" md="3" class="pa-1">
        <h4 class="font-weight-medium">Select Office</h4>
      </v-col>
      <v-col cols="12" sm="12" md="12" class="pa-1">
          <div>
            <v-autocomplete clearable v-model="office" :items="offices.state.value" label="Office"
              @update:model-value="handleOfficeChange" return-object item-title="country">
            </v-autocomplete>
          </div>
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
  props: ['offices'],

  setup(props) {
    const $router = useRouter()
    const office = ref<Api.Inputs.Office>()
    const $route = useRoute()


    const handleOfficeChange = () => {
      $router.push({ path: '/users', query: { location_id: office.value?.id } })
    }


    watch(
      () => props.offices.state.value,
      async (newValue) => {
        if ($route.query.location_id && props.offices.state.value) {
          office.value = props.offices.state.value.find((office: any) => office.id === Number($route.query.location_id));
        }
      },
    );
    return {
      office,
      handleOfficeChange
    }
  }
}
</script>
