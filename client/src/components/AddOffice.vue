<template>
  <v-container>
    <v-form ref="form" @submit.prevent="addOffice">
      <v-row class="justify-center align-center">
        <v-col cols="12">
          <v-text-field
            v-model="office.name"
            label="Name"
            type="text"
            :rules="requiredStringRules"
          ></v-text-field>
          <v-autocomplete
            label="Country"
            :items="countryList"
            v-model="selectedCountry"
            auto-select-first
          ></v-autocomplete>
          <v-select
            v-model="selectedWeekend"
            :items="weekendOptions"
            item-title="value"
            item-value="id"
            label="Weekend"
            return-object
            :rules="requiredRules"
          ></v-select>
          <v-btn color="primary" type="submit" :disabled="!form?.isValid">Add Office</v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script lang="ts">
import { ref } from 'vue'
import { $api } from '@/clients'
import { requiredRules, requiredStringRules } from '@/utils'
import { countries } from '@/utils'

export default {
  name: 'AddOffice',
  setup() {
    const form = ref()
    const weekendOptions = ref([
      {
        id: 1,
        value: 'Friday:Saturday'
      },
      {
        id: 2,
        value: 'Saturday:Sunday'
      }
    ])
    const selectedWeekend = ref(weekendOptions.value[0])
    const countryList = countries.map((c: any) => c.name)
    const selectedCountry = ref(countryList[0])
    const office = ref({
      name: '',
      country: selectedCountry.value,
      weekend: selectedWeekend.value.value
    })

    async function addOffice() {
      await $api.office.create(office.value)
    }

    return {
      form,
      office,
      weekendOptions,
      selectedWeekend,
      requiredRules,
      requiredStringRules,
      countryList,
      selectedCountry,
      addOffice
    }
  }
}
</script>
