<template>
  <v-container>
    <v-form ref="form" @submit.prevent="setVacations">
      <v-row class="justify-center align-center">
        <v-col cols="11">
          <v-text-field v-model="office_balance.year" type="number" label="Year" :rules='requiredRules'></v-text-field>
          <v-text-field
            v-model="office_balance.annual_leaves"
            type="number"
            label="Annual Leaves"
            :rules='requiredRules'
          ></v-text-field>
          <v-text-field
            v-model="office_balance.leave_excuses"
            type="number"
            label="Leave Excuses"
            :rules='requiredRules'
          ></v-text-field>
          <v-text-field
            v-model="office_balance.emergency_leaves"
            type="number"
            label="Emergency Leaves"
            :rules='requiredRules'
          ></v-text-field>
          <v-text-field
            v-model="formattedDates"
            label="Public Holidays"
            placeholder="Select or enter dates separated by commas"
            @click="toggleDatePicker" 
            :rules='requiredRules'  
            readonly  
          >
            <template v-slot:append-inner>
              <v-icon>mdi-calendar</v-icon>
            </template>
          </v-text-field>

          <v-date-picker
            v-model="selectedDates"
            multiple
            @click:prev="preventDefault"
            @click:next="preventDefault"
            v-if="datePickerVisible"
          ></v-date-picker>

          <v-btn color="primary" type="submit" :disabled="!form?.isValid"> Set Balance </v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script lang="ts">
import { $api } from '@/clients'
import type { Api } from '@/types'
import { computed, onMounted, ref } from 'vue'
import moment from "moment"
import { requiredRules } from '@/utils'

export default {
  name: 'SetVacations',
  setup() {
    const form = ref()
    const datePickerVisible = ref(false)
    const office_balance = ref<Api.Returns.GetAdminBalance>({
      annual_leaves: 0,
      compensation: 0,
      emergency_leaves: 0,
      leave_excuses: 0,
      year: 0,
      public_holidays: [],
      location: {
        id: 0,
        name: '',
        country: '',
        weekend: ''
      }
    })
    const selectedDates = ref([]);

    // const formattedDates = computed(() => {
    //   const mergedDates = [...selectedDates.value, ...office_balance.value.public_holidays].map(date => moment(date).format('YYYY-MM-DD')).join(', ');
      
    //   return mergedDates
    // })

    const formattedDates = computed(() => {
      const combinedDates = [
        ...selectedDates.value,
        ...office_balance.value.public_holidays.map(date => new Date(date))
      ];

      (selectedDates.value as any) = Array.from(new Set(combinedDates));

      return combinedDates.sort((a, b) => a.getTime() - b.getTime()).map(date => moment(date).format('YYYY-MM-DD')).join(', ');
    }); 

    onMounted(async () => {
      await $api.auth.login({
        email: 'admin@gmail.com',
        password: '0000'
      })
      office_balance.value = await $api.vacations.get_admin_balance.list()
    })

    async function setVacations() {
      const {
        annual_leaves,
        compensation,
        emergency_leaves,
        leave_excuses,
        year
      } = office_balance.value
      await $api.vacations.post_admin_balance.create({
        annual_leaves,
        compensation,
        emergency_leaves,
        leave_excuses,
        year,
        public_holidays: formattedDates.value.split(", ")
      })
    }

    function toggleDatePicker() {
      datePickerVisible.value = !datePickerVisible.value
    }

    function preventDefault(event: Event) {
      event.preventDefault()
    }
    return {
      form,
      office_balance,
      datePickerVisible,
      formattedDates,
      selectedDates,
      requiredRules,
      setVacations,
      toggleDatePicker,
      preventDefault
    }
  }
}
</script>
