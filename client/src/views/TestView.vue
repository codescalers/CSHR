<template>
  <div>
    <v-row>
      <v-col cols="2">
        <v-checkbox v-model="filters.meeting" color="#efeaea" label="Meetings" />
      </v-col>
      <v-col cols="2">
        <v-checkbox v-model="filters.event" color="#47a2ff" label="Events" />
      </v-col>
      <v-col cols="2">
        <v-checkbox v-model="filters.vacation" color="#fcd091" label="Vacations" />
      </v-col>
      <v-col cols="2">
        <v-checkbox v-model="filters.holiday" color="#5effb4" label="Holidays" />
      </v-col>
      <v-col cols="2">
        <v-checkbox v-model="filters.birthday" color="#e0adf0" label="Birthdays" />
      </v-col>
    </v-row>

    <v-row>
      <v-col class="ml-5 mr-5" v-for="event of filteredEvents" :key="event.type">
        <v-card class="pa-5" color="blue">{{ event.type }}</v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts" setup>
import { $api } from '@/clients'
import type { Api } from '@/types'
import { useAsyncState } from '@vueuse/core'
import { watch } from 'vue'
import { reactive, ref } from 'vue'

const currentDate = ref<Date>(new Date())
const events = ref<Api.Home[]>([])
const filteredEvents = ref<Api.Home[]>([])

const loadEvents = async () => {
  useAsyncState(
    () =>
      $api.home.list({
        month: currentDate.value.getMonth() + 1,
        year: currentDate.value.getFullYear()
      }),
    [],
    {
      onSuccess(data) {
        events.value = data
        filteredEvents.value = [...events.value]
      }
    }
  )
}

loadEvents()

const filters = reactive({
  meeting: true,
  event: true,
  vacation: true,
  holiday: true,
  birthday: true
})

const filterEvents = () => {  
  console.log("events.value len 1", events.value.length);
  filteredEvents.value = events.value.filter(event => {
    return (
      (event.type === 'meeting' && filters.meeting) ||
      (event.type === 'event' && filters.event) ||
      (event.type === 'vacation' && filters.vacation) ||
      (event.type === 'holiday' && filters.holiday) ||
      (event.type === 'birthday' && filters.birthday)
    );
  });
  console.log("filteredEvents", filteredEvents.value.length);
}

watch(filters, filterEvents, { deep: true })
</script>
