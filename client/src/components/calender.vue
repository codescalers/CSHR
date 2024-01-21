<template>
  <v-checkbox v-model="selected.meetings" label="Meetings" />
  <v-checkbox v-model="selected.events" label="Events" />
  <v-checkbox v-model="selected.vacations" label="Vacations" />
  <div class="ma-7 pa-7">
    <FullCalendar
      :options="{
        ...options,
        events: eventsOption
      }"
    />
  </div>

  <CustomVDialog
    v-if="dates?.startStr"
    :routeQuery="dates?.startStr"
    :modelValue="showDialog[dates?.startStr]"
  >
    <v-card>
      <calenderRequest :dates="dates" @close-dialog="closeDialog(dates?.startStr)" />
    </v-card>
  </CustomVDialog>

  <!-- <CustomVDialog
    v-if="isViewRequest && isMeeting && meeting"
    :routeQuery="meeting.id"
    :modelValue="showDialog[meeting.id]"
  >
    <v-card>
      <meetingCard :meeting="meeting" @close-dialog="closeDialog(meeting.id)" />
    </v-card>
  </CustomVDialog> -->

  <VDialog
    v-if="isViewRequest && isEvent && event"
    :routeQuery="event.name"
    :modelValue="showDialog[event.name]"
  >
    <v-card>
      <eventCard :event="event" @close-dialog="closeDialog(event.name)" />
    </v-card>
  </VDialog>

  <VDialog
    v-if="isViewRequest && isLeave && vacation"
    :routeQuery="vacation.id"
    :modelValue="showDialog[vacation.id]"
  >
    <v-card>
      <vacationCard :vacation="vacation" @close-dialog="closeDialog(vacation.id)" />
    </v-card>
  </VDialog>
</template>
<script lang="ts">
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction' // Add this line
import timeGridPlugin from '@fullcalendar/timegrid'
import FullCalendar from '@fullcalendar/vue3'
import listPlugin from '@fullcalendar/list'
import calenderRequest from '@/components/calenderRequest.vue'
import meetingCard from '@/components/cards/meetingCard.vue'
import eventCard from '@/components/cards/eventCard.vue'
import vacationCard from '@/components/cards/vacationCard.vue'

import { ref, computed } from 'vue'
import type { Api } from '@/types'
import { useApi } from '@/hooks'
import type { EventClickArg } from '@fullcalendar/core/index.js'
import type { CalendarApi } from '@fullcalendar/core/index.js'
import { useAsyncState } from '@vueuse/core'

function handelDates(start: any, end: any): any {
  const dates = {
    start,
    end,
    add: true,
    cut: null,
    endStr: null as null | string | Date,
    startStr: null as null | string | Date
  }

  const endDate = new Date(dates.end || '')
  if (dates.cut) {
    endDate.setDate(endDate.getDate() - 1)
  } else if (dates.add) {
    endDate.setDate(endDate.getDate() + 1)
  }

  dates.end = endDate
  dates.start = new Date(dates.start)

  const endStr = `${endDate.getFullYear()}-${endDate.getMonth() + 1}-${endDate.getDate()}`
  const startStr = `${dates.start.getFullYear()}-${
    dates.start.getMonth() + 1
  }-${dates.start.getDate()}`

  dates.endStr = endStr
  dates.startStr = startStr
  return dates
}

function normalizeVacation(v: Api.Vacation): any {
  const dates = handelDates(v.from_date, v.end_date)

  return {
    title: 'Vacation',
    color: 'primary',
    start: dates.start,
    end: dates.end,
    backgroundColor: 'primary',
    id: v.id.toString(),
    allDay: true
  }
}

function normalizeEvent(e: Api.Inputs.Event): any {
  const dates = handelDates(e.from_date, e.end_date)

  return {
    title: 'Event',
    color: 'primary',
    start: dates.start,
    end: dates.end,
    backgroundColor: 'primary',
    id: e.name,
    allDay: true
  }
}

function normalizeMeeting(m: Api.Meetings): any {
  const dates = handelDates(m.date, m.date)

  return {
    title: 'Meeting',
    color: 'secondary',
    start: dates.start,
    end: dates.end,
    backgroundColor: 'primary',
    id: m.id,
    allDay: true
  }
}

export default {
  name: 'calenderCshr',
  components: {
    FullCalendar,
    calenderRequest,
    // meetingCard,
    eventCard,
    vacationCard
  },

  setup() {
    const $api = useApi()
    const meetings = useAsyncState($api.meeting.list(), [])
    const events = useAsyncState($api.event.list(), [])
    const vacations = useAsyncState($api.vacations.list(), [])

    const meeting = ref<Api.Meetings>()
    const isViewRequest = ref<Boolean>(false)
    const isEvent = ref<Boolean>(false)
    const isMeeting = ref<Boolean>(false)
    const isLeave = ref<Boolean>(false)
    const event = ref<Api.Inputs.Event>()

    const vacation = ref<Api.Vacation>()
    const calendar = ref<CalendarApi>()

    const dates = ref<any>()
    console.log()

    const selected = ref({ events: true, vacations: true, meetings: true })
    const showDialog = ref<{ [key: string]: boolean }>({})
    const onSelect = async (arg: any) => {
      calendar.value = arg.view.calendar
      dates.value = arg

      openDialog(arg.startStr)
    }

    const onClick = async (arg: EventClickArg) => {
      calendar.value = arg.view.calendar

      if (arg.event.title === 'Meeting') {
        meeting.value = meetings.state.value.filter(
          (meeting) => meeting.id === Number(arg.event.id)
        )[0]
        isMeeting.value = true
        openDialog(meeting.value.id)
      } else if (arg.event.title === 'Event') {
        event.value = events.state.value.filter((event) => event.name === arg.event.id)[0]
        isEvent.value = true
        openDialog(event.value.name)
      } else if (arg.event.title === 'Vacation') {
        vacation.value = vacations.state.value.filter(
          (vacation) => vacation.id === Number(arg.event.id)
        )[0]
        isLeave.value = true
        openDialog(vacation.value.id)
      }
      isViewRequest.value = true
    }

    const plugins = [dayGridPlugin, timeGridPlugin, listPlugin, interactionPlugin] as any
    const eventsOption = computed(() => {
      return [
        ...(selected.value.meetings ? meetings.state.value.map(normalizeMeeting) : []),
        ...(selected.value.events ? events.state.value.map(normalizeEvent) : []),
        ...(selected.value.vacations ? vacations.state.value.map(normalizeVacation) : [])
      ]
    })

    const options = {
      plugins,
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
      editable: false
    }

    function closeDialog(id: string | number) {
      isViewRequest.value, isEvent.value, isMeeting.value, (isLeave.value = false)
      event.value, meeting.value, (dates.value = undefined)
      showDialog.value[id] = false
    }

    async function openDialog(id: string | number) {
      showDialog.value[id] = true
    }

    return {
      events,
      meetings,
      vacations,

      isViewRequest,
      isEvent,
      isLeave,
      isMeeting,
      meeting,
      event,
      showDialog,
      options,
      eventsOption,
      dates,
      vacation,
      selected,
      closeDialog,
      openDialog,
      onSelect,
      onClick,
      calenderRequest,
      meetingCard,
      eventCard,
      vacationCard
    }
  }
}
</script>
