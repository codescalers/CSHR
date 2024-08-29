<template>
  <v-container class="pa-6 mx-auto">
    <div class="my-6">
      <h2 class="font-weight-medium my-3">ThreeFold Offices</h2>
      <v-divider></v-divider>
    </div>
    
    <v-row v-if="isLoading" class="d-flex justify-center align-center" style="height: 750px;">
      <v-progress-circular color="primary" indeterminate :size="47"></v-progress-circular>
    </v-row>

    <div class="data" v-else-if="state?.results.length">
      <v-row>
        <v-col xl="4" lg="6" md="12" sm="12" cols="12" v-for="office in state.results" :key="office.name">
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
      <v-pagination class="mt-4 mb-4" v-model="page" :length="count" rounded="circle"></v-pagination>
    </div>
    
    <div v-else>
      <NotFoundComponent :page-not-found="false" message="Seems like there are no offices." />
    </div>
    <OfficeHolidaysDialog :selected-office="selectedOffice!" @close-dialog="closeDialog"/>
  </v-container>
</template>

<script lang="ts">
import { $api } from '@/clients'
import NotFoundComponent from '@/components/NotFoundComponent.vue'
import OfficeHolidaysDialog from '@/components/dialogs/OfficeHolidaysDialog.vue'
import type { Api } from '@/types'
import { useAsyncState } from '@vueuse/core'
import { byCountry } from "country-code-lookup"
import { capitalize, computed, ref, watch } from 'vue'

export default {
  name: 'UsersView',
  components: { NotFoundComponent, OfficeHolidaysDialog },
  setup() {
    const selectedOffice = ref<Api.LocationType | null>(null)
    const requestYears = ref(5)
    const loading = ref(false)
    const tab = ref(new Date().getFullYear())
    const holidays = ref<Api.OfficeHolidayDates[]>([])
    const isOfficeSelected = computed(() => !!selectedOffice.value)
    const page = ref(1)
    const count = computed(() => (state.value ? Math.ceil(state.value!.count / 12) : 0))
    
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
    
    const { execute, state, isLoading, } = useAsyncState(() => {
      return $api.office.list({page: page.value,});
    }, undefined, { immediate: true })

    watch(page, () => {
      console.log(page.value)
      execute();
    })

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
      page,
      count,
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
