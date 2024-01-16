<template>
  <v-container>
    <v-form ref="form" @submit.prevent="addOffice">
      <v-row class="justify-center align-center">
        <v-col cols="11">
          <v-text-field v-model="office.name" label="Name" type="text"></v-text-field>
          <v-text-field v-model="office.country" label="Country" type="text"></v-text-field>
          <v-select
            v-model="selectedWeekend"
            :items="weekendOptions"
            item-title="value"
            item-value="id"
            label="Select"
            return-object
            single-line
          ></v-select>
          <v-btn color="primary" type="submit" :disabled="!form?.isValid">Add Office</v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script lang="ts">
import { $api } from '@/clients'
import { ref } from 'vue'

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
    const office = ref({
      name: '',
      country: '',
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
      addOffice
    }
  }
}
</script>
