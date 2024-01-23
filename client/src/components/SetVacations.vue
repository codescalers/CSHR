<template>
  <v-container>
    <v-form ref="form" @submit.prevent>
      <v-row class="justify-center align-center">
        <v-col cols="12">
          <v-alert
            class="mb-3"
            type="info"
            text="The provided figures reflect the current year's details for this office. Make sure to change the year if you want to set new data. Otherwise, the existing 2024 data will be amended."
          >
          </v-alert>
          <v-alert class="mb-3" type="info" text="You need to set the data annually."></v-alert>
          <v-text-field
            v-model="office_balance.year"
            type="number"
            label="Year"
            :rules="requiredRules"
          ></v-text-field>
          <v-text-field
            v-model="office_balance.annual_leaves"
            type="number"
            label="Annual Leaves"
            :rules="requiredRules"
          ></v-text-field>
          <v-text-field
            v-model="office_balance.leave_excuses"
            type="number"
            label="Leave Excuses"
            :rules="requiredRules"
          ></v-text-field>
          <v-text-field
            v-model="office_balance.emergency_leaves"
            type="number"
            label="Emergency Leaves"
            :rules="requiredRules"
          ></v-text-field>
          <v-text-field
            v-model="formattedDates"
            label="Public Holidays"
            placeholder="Select or enter dates separated by commas"
            @click="toggleDatePicker"
            :rules="requiredRules"
            readonly
          >
            <template v-slot:append-inner>
              <v-icon>mdi-calendar</v-icon>
            </template>
          </v-text-field>

          <v-date-picker
            v-if="datePickerVisible"
            v-model="selectedDates"
            @click:prev.prevent
            @click:next.prevent
            multiple
          ></v-date-picker>

          <v-btn
            color="primary"
            type="submit"
            :disabled="!form?.isValid"
            :loading="isLoading"
            @click="execute"
          >
            Set Balance
          </v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script lang="ts">
import { $api } from '@/clients'
import type { Api } from '@/types'
import { computed, onMounted, ref } from 'vue'
import { requiredRules } from '@/utils'
import { formatDate } from '@/utils'
import { useAsyncState } from '@vueuse/core'

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
    const selectedDates = ref([
      ...office_balance.value.public_holidays.map((date) => new Date(date))
    ])

    const formattedDates = computed(() => {
      const combinedDates = [...selectedDates.value]

      return combinedDates
        .sort((a, b) => a.getTime() - b.getTime())
        .map((date) => formatDate(date))
        .join(', ')
    })

    onMounted(async () => {
      try {
        office_balance.value = await $api.vacations.get_admin_balance.list()
        selectedDates.value = [
          ...office_balance.value.public_holidays.map((date: any) => new Date(date))
        ]
      } catch (error) {
        console.error(error)
      }
    })

    function toggleDatePicker() {
      datePickerVisible.value = !datePickerVisible.value
    }

    const { execute, isLoading } = useAsyncState(
      async () => {
        const { annual_leaves, compensation, emergency_leaves, leave_excuses, year } =
          office_balance.value
        await $api.vacations.post_admin_balance.create({
          annual_leaves,
          compensation,
          emergency_leaves,
          leave_excuses,
          year,
          public_holidays: formattedDates.value.split(', ')
        })
      },
      null,
      { immediate: false }
    )

    return {
      form,
      office_balance,
      datePickerVisible,
      formattedDates,
      selectedDates,
      requiredRules,
      isLoading,
      toggleDatePicker,
      execute
    }
  }
}
</script>
