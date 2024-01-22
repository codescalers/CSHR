<!-- eslint-disable vue/no-async-in-computed-properties -->
<template>
  <v-row>
    <v-col cols="4">
      <v-checkbox v-model="selected.meetings" label="Meetings" />
    </v-col>
    <v-col cols="4">
      <v-checkbox v-model="selected.events" label="Events" />
    </v-col>
    <v-col cols="4">
      <v-checkbox v-model="selected.vacations" label="Vacations" />
    </v-col>
  </v-row>
  <div class="ma-7 pa-7">
    <VProgressCircular v-if="events.isLoading.value" />
    <FullCalendar
      v-else
      class="fc"
      :options="{
        ...options,
        events: eventsOption,
        dayCellDidMount
      }"
    />
  </div>

  <VDialog
    v-if="dates?.startStr"
    :routeQuery="dates?.startStr"
    :modelValue="showDialog[dates?.startStr]"
  >
    <v-card>
      <calenderRequest :dates="dates" @close-dialog="closeDialog(dates?.startStr)" />
    </v-card>
  </VDialog>

  <VDialog
    v-if="isViewRequest && isMeeting && meeting"
    :routeQuery="meeting.id"
    :modelValue="showDialog[meeting.id]"
  >
    <v-card>
      <meetingCard :meeting="meeting" @close-dialog="closeDialog(meeting.id)" />
    </v-card>
  </VDialog>

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
import type { EventClickArg, CalendarApi, DayCellMountArg } from '@fullcalendar/core/index.js'
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

function normalizeEvent(e: Api.Inputs.Event): any {
  const dates = handelDates(e.from_date, e.end_date)

  return {
    title: 'Event',
    classNames: ['cshr-event'],
    color: 'primary',
    start: dates.start,
    end: dates.end,
    // backgroundColor: 'offwhite',
    // backgroundColor: 'red',
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
    meetingCard,
    eventCard,
    vacationCard
  },

  setup() {
    const $api = useApi()
    const meetings = useAsyncState($api.meeting.list(), [])
    const events = useAsyncState($api.event.list(), [])
    useAsyncState($api.vacations.list(), [], {
      onSuccess(data) {
        vacations.execute(undefined, data)
      }
    })

    const vacations = useAsyncState(
      async (vacations: Api.Vacation[]) => {
        const ids = vacations.map((v) => v.applying_user)
        const users = await Promise.all(
          ids.map((id) => $api.users.getuser(id, { disableNotify: true }))
        )

        return vacations.map((v, i) => {
          v.user = users[i]
          return v
        })
      },
      [],
      { immediate: false }
    )

    const meeting = ref<Api.Meetings>()
    const isViewRequest = ref<Boolean>(false)
    const isEvent = ref<Boolean>(false)
    const isMeeting = ref<Boolean>(false)
    const isLeave = ref<Boolean>(false)
    const event = ref<Api.Inputs.Event>()

    const vacation = ref<Api.Vacation>()
    const calendar = ref<CalendarApi>()

    const dates = ref<any>()

    const selected = ref({ events: true, vacations: true, meetings: true })
    const showDialog = ref<{ [key: string]: boolean }>({})
    const onSelect = async (arg: any) => {
      calendar.value = arg.view.calendar
      dates.value = arg

      openDialog(arg.startStr)
    }
    function normalizeVacation(v: Api.Vacation) {
      const dates = handelDates(v.from_date, v.end_date)

      return {
        title: `${v.user!.full_name}'s Vacation`,
        color: 'primary',
        start: dates.start,
        end: dates.end,
        backgroundColor: 'gray',
        id: v.id.toString(),
        allDay: true
      }
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
      } else if (arg.event.title.includes('Vacation')) {
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
      const normalizedMeetings = selected.value.meetings
        ? meetings.state.value.map(normalizeMeeting)
        : []
      const normalizedEvents = selected.value.events ? events.state.value.map(normalizeEvent) : []
      const normalizedVacations = selected.value.vacations
        ? vacations.state.value.map(normalizeVacation)
        : []

      return [...normalizedMeetings, ...normalizedEvents, ...normalizedVacations]
    })

    function dayCellDidMount({ el, date }: DayCellMountArg) {
      for (const event of events.state.value) {
        const current = date.getTime()
        const start = new Date(event.from_date).getTime() - 86_400_000
        const end = new Date(event.end_date).getTime()

        const shouldUpdate = current >= start && current <= end
        if (shouldUpdate) {
          el.style.backgroundColor = 'rgba(255, 255, 255, 0.05)'
          return
        }
      }
    }

    async function getUser(id: any) {
      const user = await $api.users.getuser(id, { disableNotify: true })
      return user.first_name
    }

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
      dayCellDidMount,
      closeDialog,
      openDialog,
      onSelect,
      onClick,
      getUser,
      calenderRequest,
      meetingCard,
      eventCard,
      vacationCard
    }
  }
}
</script>

<style scoped>
.fc-bg-event {
  background: hsl(302, 90%, 49%);
  border: 1px solid #0d89ec;
  color: #ffffff;
}
</style>
