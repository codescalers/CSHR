<template>
  <v-dialog
    v-model="isOfficeSelected"
    route-query="office"
    max-width="1000"
    @click:outside="closeDialog"
  >
    <v-card>
      <v-card-title>{{
        selectedOffice ? capitalize(selectedOffice.name) + ' Office' : 'Office Details'
      }}</v-card-title>
      <v-card-text>
        <v-alert class="mb-4">{{
          selectedOffice ? capitalize(selectedOffice!.name) + ' public holidays' : 'Public holidays'
        }}</v-alert>
        <div class="d-flex flex-row">
          <v-tabs v-model="tab" color="primary" direction="vertical">
            <!-- <v-text-field
            style="max-width: 150px;"
            v-model="requestYears"
            variant="underlined"
            label="Last years"
            color="primary"
            :rules="[
              (v: string) => !isNaN(+v) || 'Please enter only numeric values in this field.',
              (v: string) => +v <= 7 || 'The value should not be more than 7.',
              (v: string) => +v >= 1 || 'The value should not be less than 1.'
            ]"
          /> -->
            <v-tab
              v-for="year in getYears({
                years: requestYears >= 1 && requestYears <= 7 ? requestYears : 5
              })"
              :key="year"
              prepend-icon="mdi-calendar-range"
              :text="year.toFixed()"
              :value="year"
            >
            </v-tab>
          </v-tabs>
          <v-card class="pa-4 pt-1 ml-4 w-100">
            <v-toolbar
              class="w-100 d-felx justify-center"
              color="primary"
              height="30"
              style="border-radius: 3px"
            >
              <strong class="text-center ml-4"
                >Filtering the total public holidays based on the year {{ tab }}.</strong
              >
            </v-toolbar>
            <v-card class="pa-4">
              <div class="" v-if="holidays.length">
                <v-chip
                  class="mr-2 ml-2 mt-2"
                  color="success"
                  v-for="date in holidays"
                  :key="date.holiday_date"
                  >{{ date.holiday_date }}</v-chip
                >
              </div>
              <div class="" v-else>
                <p>Seems like no public holidays were found for this year.</p>
              </div>
            </v-card>
          </v-card>
        </div>
      </v-card-text>
      <v-divider class="mt-2 mb-4"></v-divider>
      <div class="d-flex justify-end align-center mb-0 pb-0">
        <v-btn
          color="white"
          text="Close"
          @click="closeDialog"
          class="btn-capitalize mb-4 mr-4"
        ></v-btn>
      </div>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { $api } from '@/clients'
import type { Api } from '@/types'
import { useAsyncState } from '@vueuse/core'
import { capitalize, computed, onMounted, ref, watch, type PropType } from 'vue'

export default {
  name: 'UsersView',
  props: {
    selectedOffice: {
      type: Object as PropType<Api.LocationType>,
      required: true
    },
    showDialog: Boolean
  },
  emits: ['closeDialog'],
  setup(props, { emit }) {
    const requestYears = ref(5)
    const tab = ref()
    const holidays = ref<Api.OfficeHolidayDates[]>([])
    const isOfficeSelected = computed(() => !!props.selectedOffice)

    const closeDialog = (): void => {
      emit('closeDialog', false)
      tab.value = new Date().getFullYear()
    }

    const getYears = (options: { years: number }): number[] => {
      const thisYear = new Date().getFullYear()
      return Array.from({ length: options.years }, (_, i) => thisYear - i)
    }

    function listHolidays() {
      return useAsyncState(
        $api.office.officeHolidays({ year: tab.value, office_id: props.selectedOffice.id }),
        [],
        { immediate: true }
      )
    }

    onMounted(() => {
      tab.value = new Date().getFullYear()
    })

    watch(tab, async () => {
      holidays.value = []
      const req = listHolidays()
      await req.execute()
      holidays.value = req.state.value
    })

    return {
      isOfficeSelected,
      tab,
      requestYears,
      holidays,

      getYears,
      closeDialog,
      capitalize
    }
  }
}
</script>
<style></style>
