<template>
  <v-row class="justify-center py-4">
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
  <v-divider class="d-flex mx-auto" style="width: 90%"></v-divider>

  <div class="ma-7 px-7">
    {{ isLoading }}
    <div class="loading-container d-flex align-center justify-center my-5" v-if="isLoading">
      <v-alert density="compact" class="pa-5" type="info" text="Events are loading..."></v-alert>
    </div>

    <FullCalendar
      class="fc"
      :options="{
        ...options,
        events: filteredEvents as any
      }"
    >
    </FullCalendar>

  </div>
</template>

<script lang="ts" setup>
import { reactive, ref, watch } from 'vue'
import { type CalendarOptions } from '@fullcalendar/core'
import { useApi } from '@/hooks'
import { useAsyncState } from '@vueuse/core'

import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import listPlugin from '@fullcalendar/list'
import interactionPlugin from '@fullcalendar/interaction'
import type { Api } from '@/types'
import { normalizeEvent, normalizeVacation } from '@/utils/helpers'
import { normalizedBirthday, normalizeHoliday, normalizeMeeting } from '@/utils'

const homeEvents = ref<Api.Home[]>([])
const filteredEvents = ref<Api.Home[]>([])

const currentDate = ref<Date>(new Date())
const isLoading = ref<boolean>(false)
const $api = useApi()
const filters = reactive({
  meeting: true,
  event: true,
  vacation: true,
  holiday: true,
  birthday: true
})

const loadEvents = async () => {
  isLoading.value = true
  useAsyncState(
    () =>
      $api.home.list({
        month: currentDate.value.getMonth() + 1,
        year: currentDate.value.getFullYear()
      }),
    [],
    {
      onSuccess(data) {
        console.log("data", data);
        
        for (const event of data) {
          updateEventCalendarType(event)
        }
        filteredEvents.value = [...homeEvents.value]
        console.log(filteredEvents.value);
      }
    }
  )
  isLoading.value = false
}

const updateEventCalendarType = (event: any) => {
  if (event.type === 'vacation') {
    const vacationEvent = normalizeVacation(event) as any
    homeEvents.value.push(vacationEvent)
  } else if (event.type === 'holiday') {
    const publicHoliday = normalizeHoliday(event) as any
    homeEvents.value.push(publicHoliday)
  } else if (event.type === 'meeting') {
    const meeting = normalizeMeeting(event) as any
    homeEvents.value.push(meeting)
  } else if (event.type === 'birthday') {
    const birthday = normalizedBirthday(event) as any
    homeEvents.value.push(birthday)
  } else if (event.type === 'event') {
    const _event = normalizeEvent(event) as any
    homeEvents.value.push(_event)
  }

  filteredEvents.value = [...homeEvents.value]
}

const filterEvents = () => {  
  console.log("events.value len 1", homeEvents.value.length);
  filteredEvents.value = homeEvents.value.filter(event => {
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


function onSelect() {}
function onClick() {}

const options = reactive<CalendarOptions>({
  plugins: [dayGridPlugin, timeGridPlugin, listPlugin, interactionPlugin],
  // dayMaxEventRows: true,
  dayMaxEvents: true,
  initialView: 'dayGridMonth',
  headerToolbar: {
    left: 'prev,next today',
    center: 'title',
    right: 'dayGridMonth,dayGridWeek,listDay'
  },
  selectable: true,
  weekends: true,
  select: onSelect,
  eventClick: onClick,
  events: [],
  editable: false,
  datesSet: (arg) => (currentDate.value = arg.view.currentStart)
})

watch(currentDate, () => loadEvents(), { deep: true })
watch(filters, filterEvents, { deep: true })
</script>

<style>
.fc {
  font-size: 0.875rem !important;
}

.fc-theme-standard .fc-scrollgrid {
  border: 1px solid #3c3c3c !important;
}

.fc-theme-standard td,
.fc-theme-standard th {
  border: 1px solid #3c3c3c !important;
}

.fc .fc-button .fc-icon {
  font-size: 1em;
  vertical-align: baseline;
}

.fc-daygrid-block-event .fc-event-time,
.fc-daygrid-block-event .fc-event-title {
  padding: 1px 9px;
}

button {
  text-transform: capitalize !important;
}

.fc-event-title {
  font-weight: 500;
  color: #131313 !important;
}

.fc-popover {
  background-color: rgb(49 47 47) !important;
  color: #ffffff;

  .fc-popover-header {
    background-color: rgb(100, 99, 99) !important;
  }
}
</style>
