<template>
  <v-row class="justify-center py-4">
    <v-col cols="2">
      <v-checkbox v-model="filters.vacation" color="#fcd091" label="Vacations" />
    </v-col>
    <v-col cols="2">
      <v-checkbox v-model="filters.meeting" color="#efeaea" label="Meetings" />
    </v-col>
    <v-col cols="2">
      <v-checkbox v-model="filters.event" color="#47a2ff" label="Events" />
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

  <!-- Dialogs -->
  <!-- Create new event dialog -->
  <v-dialog
    v-if="selectedEventType.isNewEvent"
    :routeQuery="dates?.startStr"
    :modelValue="selectedEventType.isNewEvent"
    @click:outside="closeDialog(CalendarEventSelection.NewEvent)"
  >
    <v-card>
      <calender-request :dates="dates" @close-dialog="closeDialog(CalendarEventSelection.NewEvent)"
        @create-vacation="createVacation($event)" @create-meeting="createMeeting($event)"
        @create-event="createEvent($event)" />
    </v-card>
  </v-dialog>

  <!-- View meeting dialog -->
  <v-dialog v-if="selectedEventType.isViewRequest && selectedEventType.isMeeting && selectedEvent"
    :routeQuery="selectedEvent.id" :modelValue="selectedEventType.isMeeting">
    <v-card>
      <meeting-card :meeting="selectedEvent" @close-dialog="closeDialog(CalendarEventSelection.Meeting)" />
    </v-card>
  </v-dialog>

  <!-- View holiday dialog -->
  <v-dialog v-if="selectedEventType.isViewRequest && selectedEventType.isHoliday && selectedEvent"
    :routeQuery="selectedEvent.id" :modelValue="selectedEventType.isHoliday">
    <v-card>
      <holiday-card :holiday="selectedEvent" @close-dialog="closeDialog(CalendarEventSelection.PublicHoliday)" />
    </v-card>
  </v-dialog>

  <!-- View holiday dialog -->
  <v-dialog v-if="selectedEventType.isViewRequest && selectedEventType.isBirthday && selectedEvent"
    :routeQuery="selectedEvent.id" :modelValue="selectedEventType.isBirthday">
    <v-card>
      <birthday-card :birthday="selectedEvent" @close-dialog="closeDialog(CalendarEventSelection.Birthday)" />
    </v-card>
  </v-dialog>

  <!-- View event dialog -->
  <v-dialog v-if="selectedEventType.isViewRequest && selectedEventType.isEvent && selectedEvent"
    :routeQuery="selectedEvent.id" :modelValue="selectedEventType.isEvent">
    <v-card>
      <event-card :event="selectedEvent" @close-dialog="closeDialog(CalendarEventSelection.Event)" />
    </v-card>
  </v-dialog>

  <!-- View vacation dialog -->
  <v-dialog
    v-if="selectedEventType.isViewRequest && selectedEventType.isVacation && selectedEvent"
    :routeQuery="selectedEvent"
    :modelValue="selectedEventType.isVacation"
  >
    <v-card>
      <vacation-card
      :vacation="(selectedEvent as Api.Vacation)"
        @close-dialog="closeDialog(CalendarEventSelection.Vacation)"
        @status-vacation="updateVacationStatus($event)"
        @update-vacation="updateVacation($event)"
        @delete-vacation="deleteVacation()" />
    </v-card>
  </v-dialog>
</template>

<script lang="ts" setup>
import { reactive, ref, watch } from 'vue'
import { type CalendarApi, type CalendarOptions } from '@fullcalendar/core'
import { useApi } from '@/hooks'
import { useAsyncState } from '@vueuse/core'
import calenderRequest from '@/components/calenderRequest.vue'
import meetingCard from '@/components/cards/meetingCard.vue'
import holidayCard from '@/components/cards/holidayCard.vue'
import birthdayCard from '@/components/cards/birthdayCard.vue'
import vacationCard from '@/components/cards/vacationCard.vue'
import eventCard from '@/components/cards/eventCard.vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import listPlugin from '@fullcalendar/list'
import interactionPlugin from '@fullcalendar/interaction'
import { CalendarEventSelection, type Api } from '@/types'
import { normalizeEvent, normalizeVacation } from '@/utils/helpers'
import { normalizedBirthday, normalizeHoliday, normalizeMeeting } from '@/utils'
import { ApiClientBase } from '@/clients/api/base'

const homeEvents = ref<Api.Home[]>([])
const filteredEvents = ref<Api.Home[]>([])

const currentDate = ref<Date>(new Date())
const calendar = ref<CalendarApi>()
const isLoading = ref<boolean>(false)
const $api = useApi()
const dates = ref<any>()

const filters = reactive({
  meeting: true,
  event: true,
  vacation: true,
  holiday: true,
  birthday: true
})

const selectedEventType = reactive({
  isMeeting: false,
  isEvent: false,
  isVacation: false,
  isHoliday: false,
  isBirthday: false,
  isNewEvent: false,
  isViewRequest: false
})

const meetings = ref<Api.Meeting[]>([])
const events = ref<Api.Event[]>([])
const vacations = ref<Api.Vacation[]>([])
const holidays = ref<Api.Holiday[]>([])
const birthdays = ref<Api.User[]>([])
const cached_users = new Map<number, Api.User>()

const selectedEvent = ref<Api.Meeting | Api.Event | Api.Vacation | Api.Holiday | Api.User>()

const me = ApiClientBase.user.value?.fullUser

if (me) {
  cached_users.set(me.id, me)
}

const loadEvents = async () => {
  isLoading.value = true
  await useAsyncState(
    () =>
      $api.home.list({
        month: currentDate.value.getMonth() + 1,
        year: currentDate.value.getFullYear()
      }),
    [],
    {
      onSuccess(data) {
        for (const event of data) {
          updateEventCalendarType(event)
        }
        filteredEvents.value = [...homeEvents.value]
      }
    }
  )
  isLoading.value = false
}

const updateEventCalendarType = (event: any) => {
  if (event.type === 'vacation') {
    const vacationEvent = normalizeVacation(event) as any
    homeEvents.value.push(vacationEvent)
    vacations.value.push(event)
  } else if (event.type === 'holiday') {
    const publicHoliday = normalizeHoliday(event) as any
    homeEvents.value.push(publicHoliday)
    holidays.value.push(event)
  } else if (event.type === 'meeting') {
    const meeting = normalizeMeeting(event) as any
    homeEvents.value.push(meeting)
    meetings.value.push(event)
  } else if (event.type === 'birthday') {
    const birthday = normalizedBirthday(event) as any
    homeEvents.value.push(birthday)
    birthdays.value.push(event)
  } else if (event.type === 'event') {
    const _event = normalizeEvent(event) as any
    homeEvents.value.push(_event)
    events.value.push(event)
  }

  filteredEvents.value = [...homeEvents.value]
}

const filterEvents = () => {
  filteredEvents.value = homeEvents.value.filter((event) => {
    return (
      (event.type === 'meeting' && filters.meeting) ||
      (event.type === 'event' && filters.event) ||
      (event.type === 'vacation' && filters.vacation) ||
      (event.type === 'holiday' && filters.holiday) ||
      (event.type === 'birthday' && filters.birthday)
    )
  })
}

function onSelect(arg: any) {
  calendar.value = arg.view.calendar
  dates.value = arg
  openDialog(CalendarEventSelection.NewEvent)
}

function onClick(arg: any) {
  selectedEvent.value = undefined
  calendar.value = arg.view.calendar
  const clickedEventTitle = arg.event.title as string

  // We use a normalized event ID to avoid duplication. It's created by concatenating 'holiday', 'birthday', 'event', 'meeting', and 'vacation' with the event ID.
  if (clickedEventTitle.includes(CalendarEventSelection.PublicHoliday)) {
    selectedEvent.value = holidays.value.filter(
      (holiday) => holiday.id === Number(arg.event.id.replace('holiday', ''))
    )[0]

    openDialog(CalendarEventSelection.PublicHoliday)
  } else if (
    clickedEventTitle
      .toLocaleLowerCase()
      .includes(CalendarEventSelection.Vacation.toLocaleLowerCase())
  ) {
    selectedEvent.value = vacations.value.filter(
      (vacation) => vacation.id === Number(arg.event.id.replace('vacation', ''))
    )[0]
    openDialog(CalendarEventSelection.Vacation)
  } else if (clickedEventTitle.includes(CalendarEventSelection.Birthday)) {
    selectedEvent.value = birthdays.value.filter(
      (birthday) => birthday.id === Number(arg.event.id.replace('birthday', ''))
    )[0]
    openDialog(CalendarEventSelection.Birthday)
  } else if (clickedEventTitle === CalendarEventSelection.Event) {
    selectedEvent.value = events.value.filter(
      (event) => event.id === Number(arg.event.id.replace('event', ''))
    )[0]
    openDialog(CalendarEventSelection.Event)
  } else if (clickedEventTitle === CalendarEventSelection.Meeting) {
    selectedEvent.value = meetings.value.filter(
      (meeting) => meeting.id === Number(arg.event.id.replace('meeting', ''))
    )[0]
    openDialog(CalendarEventSelection.Meeting)
  }
  selectedEventType.isViewRequest = true
}

function openDialog(dialogType: CalendarEventSelection) {
  if (dialogType === CalendarEventSelection.Birthday) {
    selectedEventType.isBirthday = true
  } else if (dialogType === CalendarEventSelection.Event) {
    selectedEventType.isEvent = true
  } else if (dialogType === CalendarEventSelection.Meeting) {
    selectedEventType.isMeeting = true
  } else if (dialogType === CalendarEventSelection.PublicHoliday) {
    selectedEventType.isHoliday = true
  } else if (dialogType === CalendarEventSelection.Vacation) {
    selectedEventType.isVacation = true
  } else if (dialogType === CalendarEventSelection.NewEvent) {
    selectedEventType.isNewEvent = true
  }
}

function closeDialog(dialogType: CalendarEventSelection) {
  if (dialogType === CalendarEventSelection.Birthday) {
    selectedEventType.isBirthday = false
  } else if (dialogType === CalendarEventSelection.Event) {
    selectedEventType.isEvent = false
  } else if (dialogType === CalendarEventSelection.Meeting) {
    selectedEventType.isMeeting = false
  } else if (dialogType === CalendarEventSelection.PublicHoliday) {
    selectedEventType.isHoliday = false
  } else if (dialogType === CalendarEventSelection.Vacation) {
    selectedEventType.isVacation = false
  } else if (dialogType === CalendarEventSelection.NewEvent) {
    selectedEventType.isNewEvent = false
  }
}

async function createVacation(vacation: Api.Vacation) {
  if (cached_users.has(vacation.applying_user.id)) {
    vacation.applying_user = cached_users.get(vacation.applying_user.id)
  } else {
    const user = await $api.users.getuser(vacation.applying_user.id, { disableNotify: true })
    cached_users.set(vacation.applying_user.id, user)
    vacation.applying_user = user
  }

  vacations.value.push(vacation)

  if(window.connections.ws.value){
    window.connections.ws.value!.send(
      JSON.stringify(
        {
          event: "post_new_vacation_request",
          vacation
        }
      )
    )
  }

  const vacationEvent = normalizeVacation(vacation) as any
  filteredEvents.value.push(vacationEvent)
  closeDialog(CalendarEventSelection.NewEvent)
}

async function createMeeting(meeting: Api.Meeting) {
  meetings.value.push(meeting)
  const meetingEvent = normalizeMeeting(meeting) as any
  filteredEvents.value.push(meetingEvent)
  closeDialog(CalendarEventSelection.NewEvent)
}

async function createEvent(event: Api.Event) {
  events.value.push(event)
  const eventData = normalizeEvent(event) as any
  filteredEvents.value.push(eventData)
  closeDialog(CalendarEventSelection.NewEvent)
}

async function updateVacationStatus(data: string) {
  const vacationIndex = vacations.value.findIndex((vacation) => vacation.id === selectedEvent.value!.id)
  if (vacationIndex !== -1) {
    if (data === 'Approve') {
      vacations.value[vacationIndex].status = 'approved'
    } else;
    if (data === 'Reject') {
      vacations.value[vacationIndex].status = 'rejected'
    }
  }
  closeDialog(CalendarEventSelection.Vacation)
}

async function updateVacation(vacation: Api.Vacation) {
  vacations.value = vacations.value.filter((vacation) => vacation.id !== selectedEvent.value?.id)
  filteredEvents.value = filteredEvents.value.filter(event => event.id.toString() !== `vacation${selectedEvent.value?.id}`)

  if (cached_users.has(vacation.applying_user)) {
    vacation.applying_user = cached_users.get(vacation.applying_user)
  } else {
    const user = await $api.users.getuser(vacation.applying_user, { disableNotify: true })
    cached_users.set(vacation.applying_user, user)
    vacation.applying_user = user
  }
  vacation.type="vacation"
  vacations.value.push(vacation)
  const vacationEvent = normalizeVacation(vacation) as any
  filteredEvents.value.push(vacationEvent)
  closeDialog(CalendarEventSelection.Vacation)
}


async function deleteVacation() {
  vacations.value = vacations.value.filter((vacation) => vacation.id !== selectedEvent.value?.id)  
  filteredEvents.value = filteredEvents.value.filter(event => event.id.toString() !== `vacation${selectedEvent.value?.id}`)
  closeDialog(CalendarEventSelection.Vacation)
}

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

.fc-daygrid-event-harness {
  cursor: pointer;
}

.fc-event-title {
  font-weight: 500;
  color: #131313 !important;
  cursor: pointer;
}

.fc-popover {
  background-color: rgb(49 47 47) !important;
  color: #ffffff;

  .fc-popover-header {
    background-color: rgb(100, 99, 99) !important;
  }
}
</style>
