<template>
  <div>
    <v-card class="ma-5 pa-2 border rounded ma-2 align-self-start">
      <v-row class="ma-5">
        <v-col cols="12" class="py-5 px-2">
          <span>You can change the selected office to discover the team in other offices, current elected office is your
            office.
          </span>
        </v-col>
      </v-row>
      <v-row class="ma-5">
        <v-col cols="12" sm="12" md="2" class="px-2 align-self-start">

          <div>
            <h3> Select Office</h3>
          </div>
        </v-col>
        <v-col cols="12" sm="12" md="10" class="pa-2 border rounded  align-self-start">
          <div>
            <v-autocomplete v-model="country" :items="countriesSet" label="Default"></v-autocomplete>
          </div>

        </v-col>
      </v-row>
    </v-card>

  </div>
</template>

<script lang="ts">
import { computed, onMounted, ref } from 'vue';


export default {
  name: 'officeFilters',
  props: ["countriesSet"],

  setup(props) {
    const country = ref<string>(props.countriesSet[0]);
    //   const country = computed(() => {
    //   if (props.countriesSet.length != 0) {
    //     console.log("countries",props.countriesSet);
    //     return props.countriesSet[0];
    //     // let val = String(user.value.full_name);
    //     // return val.charAt(0);
    //   }
    //   return "";
    // });


    return {
      country,
      // avatar,
    }
  }
}
</script>

