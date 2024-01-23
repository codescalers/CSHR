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
    <FullCalendar v-else class="fc" :options="{
      ...options,
      events: eventsOption,
      dayCellDidMount
    }" />
  </div>

  <VDialog v-if="dates?.startStr" :routeQuery="dates?.startStr" :modelValue="showDialog[dates?.startStr]">
    <v-card>
      <calenderRequest :dates="dates" @close-dialog="closeDialog(dates?.startStr)"
        @update-vacation="updateVacation(dates?.startStr)" @update-meeting="updateMeeting(dates?.startStr)"
        @update-event="updateEvent(dates?.startStr)" />
    </v-card>
  </VDialog>

  <VDialog v-if="isViewRequest && isMeeting && meeting" :routeQuery="meeting.id" :modelValue="showDialog[meeting.id]">
    <v-card>
      <meetingCard :meeting="meeting" @close-dialog="closeDialog(meeting.id)" />
    </v-card>
  </VDialog>

  <VDialog v-if="isViewRequest && isEvent && event" :routeQuery="event.name" :modelValue="showDialog[event.name]">
    <v-card>
      <eventCard :event="event" @close-dialog="closeDialog(event.name)" />
    </v-card>
  </VDialog>

  <VDialog v-if="isViewRequest && isLeave && vacation" :routeQuery="vacation.id" :modelValue="showDialog[vacation.id]">
    <v-card>
      <vacationCard :vacation="vacation" @close-dialog="closeDialog(vacation.id)"
        @update-vacation="updateVacation(vacation.id)" />
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
import { normalizeEvent, normalizeVacation, normalizeMeeting } from '@/utils'




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
    const meetings = useAsyncState(() => $api.meeting.list(), [])
    const events = useAsyncState(() => $api.event.list(), [])

    const loadVacations = useAsyncState(() => $api.vacations.list(), [], {
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
      for (const event of eventsOption.value) {
        const current = date.getTime()
        const start = new Date(event.start).getTime() - 86_400_000
        const end = new Date(event.end).getTime()

        const shouldUpdate = current >= start && current <= end
        if (shouldUpdate) {
          el.style.backgroundColor = 'rgba(255, 255, 255, 0.05)'
          return
        }
      }
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

    async function updateVacation(id: number |string) {
      loadVacations.execute()
      closeDialog(id)

    }


    async function updateMeeting(id: number | string) {
      meetings.execute()
      closeDialog(id)

    }
    async function updateEvent(id: number | string) {
      events.execute()
      closeDialog(id)

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
      updateVacation,
      updateMeeting,
      updateEvent,
      calenderRequest,
      meetingCard,
      eventCard,
      vacationCard
    }
  }
}
</script>