<template>
  <v-container class="pa-6 mx-auto">
    <div class="my-6">
      <h2 class="font-weight-medium my-3">ThreeFold Offices</h2>
      <v-divider></v-divider>
    </div>
    
    <v-row v-if="isLoading" class="d-flex justify-center align-center" style="height: 750px;">
      <v-progress-circular color="primary" indeterminate :size="47"></v-progress-circular>
    </v-row>
    
    <v-row v-else-if="state.length">
      <v-col xl="4" lg="6" md="12" sm="12" cols="12" v-for="office in state" :key="office.name">
        <v-card class="pa-4 hover-card border bg-graytitle">
          <v-card-title>
            <v-row>
              <v-col cols="2">
                <v-img v-if="isCustomIcon(office)" alt="Office Country" :src="getCountryFlagSrc(office)" />
                <v-icon v-else size="50" color="primary">mdi-office-building</v-icon>
              </v-col>
              <v-col>
                <p style="margin-left: -15px;">{{ office.name.length > 30 ? capitalize(office.name).slice(0, 30) + '...' : capitalize(office.name)}}</p>
              </v-col>
            </v-row>
          </v-card-title>
          <v-card-text>
            <div class="d-flex details mt-4">
              <p class="mr-2">Location:</p>
              <strong>{{ office.country }}</strong>
            </div>
            <div class="d-flex details mt-2">
              <p class="mr-2">Weekend:</p>
              <strong>{{ formatWeekend(office.weekend) }}</strong>
            </div>
          </v-card-text>
          <v-divider class="mt-2 mb-4"></v-divider>
          <div class="d-flex justify-end align-center mb-0 pb-0">
            <v-btn @click="viewOffice(office)" color="primary" class="btn-capitalize">View</v-btn>
          </div>
        </v-card>
      </v-col>
    </v-row>
    
    <div v-else>
      <NotFoundComponent :page-not-found="false" message="Seems like there are no offices." />
    </div>
    
    <v-dialog v-model="isOfficeSelected" route-query="office" max-width="1000" @click:outside="closeDialog">
      <v-card>
        <v-card-title>{{ selectedOffice ? capitalize(selectedOffice.name) + ' Office': 'Office Details' }}</v-card-title>
        <v-card-text>
          <v-alert class="mb-4">{{selectedOffice ? capitalize(selectedOffice!.name) + ' public holidays' : 'Public holidays'}}</v-alert>
          <div class="d-flex flex-row">
            <v-tabs
              v-model="tab"
              color="primary"
              direction="vertical"
            >
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
                v-for="year in getYears({years: requestYears >= 1 && requestYears <= 7 ? requestYears : 5})"
                :key="year"
                prepend-icon="mdi-calendar-range"
                :text="year.toFixed()"
                :value="year">
              </v-tab>
            </v-tabs>
            <v-card class="pa-4 pt-1 ml-4 w-100">
              <v-toolbar class="w-100 d-felx justify-center" color="primary" height="30" style="border-radius: 3px;">
                <strong class="text-center ml-4">Filtering the total public holidays based on the year {{ tab }}.</strong>
              </v-toolbar>
              <v-card class="pa-4">
                <v-chip class="mr-2 ml-2 mt-2" color="success" v-for="date in holidays" :key="date">{{date.holiday_date}}</v-chip>
              </v-card>
            </v-card>
          </div>
        </v-card-text>
        <v-divider class="mt-2 mb-4"></v-divider>
        <div class="d-flex justify-end align-center mb-0 pb-0">
          <v-btn color="white" text="Close" @click="closeDialog" class="btn-capitalize mb-4 mr-4"></v-btn>
        </div>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import { $api } from '@/clients'
import NotFoundComponent from '@/components/NotFoundComponent.vue'
import type { Api } from '@/types'
import { useAsyncState } from '@vueuse/core'
import { byCountry } from "country-code-lookup"
import { capitalize, computed, ref, watch } from 'vue'

export default {
  name: 'UsersView',
  components: { NotFoundComponent },
  setup() {
    const selectedOffice = ref<Api.LocationType | null>(null)
    const requestYears = ref(5)
    const loading = ref(false)
    const tab = ref(new Date().getFullYear())
    const holidays = ref<Api.OfficeHolidayDates[]>([])
    const isOfficeSelected = computed(() => !!selectedOffice.value)
    const { isLoading, state } = useAsyncState($api.office.list(), [], { immediate: true })

    const getOfficeCountry = (office: Api.LocationType): string => {
      const country = byCountry(office.country)
      return country?.internet ?? office.country
    }

    const getCountryFlagSrc = (office: Api.LocationType): string => {
      const countryCode = getOfficeCountry(office).toLowerCase()
      return countryCode !== 'ch'
        ? `https://www.worldatlas.com/r/w425/img/flag/${countryCode}-flag.jpg`
        : `https://www.worldatlas.com/r/w425/img/flag/${countryCode}-flag.png`
    }

    const isCustomIcon = (office: Api.LocationType): boolean => getOfficeCountry(office) !== office.country

    const formatWeekend = (weekend: string): string => weekend.replace(':', ' and ')

    const viewOffice = (office: Api.LocationType): void => {
      selectedOffice.value = office
    }

    const closeDialog = (): void => {
      selectedOffice.value = null
      tab.value = new Date().getFullYear();
    }

    watch(selectedOffice, () => {
      isOfficeSelected.value
    })

    const getYears = (options: {years: number}): number[] => {
      const thisYear = new Date().getFullYear()
      return Array.from({ length: options.years }, (_, i) => thisYear - i)
    }

    watch([selectedOffice, tab,], async () => {
      holidays.value = [];
      if(selectedOffice.value){
        const req = useAsyncState(
          $api.office.officeHolidays({year: tab.value, office_id: selectedOffice.value.id}),
          [],
          { immediate: true }
        )
        await req.execute()
        holidays.value = req.state.value
        loading.value = isLoading.value
      }
    })



    return {
      state,
      isLoading,
      selectedOffice,
      isOfficeSelected,
      tab,
      requestYears,
      holidays,

      getYears,
      getCountryFlagSrc,
      isCustomIcon,
      formatWeekend,
      viewOffice,
      closeDialog,
      capitalize,
    }
  }
}
</script>
<style>
.btn-capitalize{
  text-transform: capitalize !important;
}
</style>
