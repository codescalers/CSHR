<!-- eslint-disable vue/no-async-in-computed-properties -->
<template>
  <v-row class="justify-center py-4">
    <v-col cols="2">
      <v-checkbox v-model="selected.meetings" color="secondary" label="Meetings" />
    </v-col>
    <v-col cols="2">
      <v-checkbox v-model="selected.events" color="gray" label="Events" />
    </v-col>
    <v-col cols="2">
      <v-checkbox v-model="selected.vacations" color="primary" label="Vacations" />
    </v-col>
    <v-col cols="2">
      <v-checkbox v-model="selected.holidays" color="#33b679" label="Holidays" />
    </v-col>
    <v-col cols="2">
      <v-checkbox v-model="selected.birthdays" color="warning" label="Birthdays" />
    </v-col>
  </v-row>
  <v-divider class="d-flex mx-auto" style="width: 90%"></v-divider>
  <div class="ma-7 px-7">
    <div
      class="loading-container d-flex align-center justify-center my-5"
      v-if="homes.isLoading.value"
    >
      <v-alert density="compact" class="pa-5" type="info" text="Events are loading..."></v-alert>
    </div>
    <FullCalendar
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
      <calenderRequest
        :dates="dates"
        @close-dialog="closeDialog(dates?.startStr)"
        @create-vacation="createVacation(dates?.startStr, $event)"
        @create-meeting="createMeeting(dates?.startStr, $event)"
        @create-event="createEvent(dates?.startStr, $event)"
      />
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
    v-if="isViewRequest && isHoliday && holiday"
    :routeQuery="holiday.id"
    :modelValue="showDialog[holiday.id]"
  >
    <v-card>
      <holidayCard :holiday="holiday" @close-dialog="closeDialog(holiday.id)" />
    </v-card>
  </VDialog>

  <VDialog
    v-if="isViewRequest && isBirthday && birthday"
    :routeQuery="birthday.id"
    :modelValue="showDialog[birthday.id]"
  >
    <v-card>
      <birthdayCard :birthday="birthday" @close-dialog="closeDialog(birthday.id)" />
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
      <vacationCard
        :vacation="vacation"
        @close-dialog="closeDialog(vacation.id)"
        @status-vacation="updateVacationStatus(vacation.id, $event)"
        @update-vacation="updateVacation(vacation.id, $event)"
        @delete-vacation="deleteVacation(vacation.id)"
      />
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
import holidayCard from '@/components/cards/holidayCard.vue'
import birthdayCard from '@/components/cards/birthdayCard.vue'

import { ref, computed, reactive, watch } from 'vue'
import type { Api } from '@/types'
import { useApi } from '@/hooks'
import type {
  EventClickArg,
  CalendarApi,
  DayCellMountArg,
  CalendarOptions
} from '@fullcalendar/core/index.js'
import { useAsyncState } from '@vueuse/core'
import {
  normalizeEvent,
  normalizeVacation,
  normalizeMeeting,
  normalizeHoliday,
  normalizedBirthday
} from '@/utils'

export default {
  name: 'calenderCshr',
  components: {
    FullCalendar,
    calenderRequest,
    meetingCard,
    eventCard,
    vacationCard,
    holidayCard,
    birthdayCard
  },

  setup() {
    const $api = useApi()
    const meeting = ref<Api.Meetings>()
    const currentDate = ref<Date>(new Date())
    const isViewRequest = ref<Boolean>(false)
    const isEvent = ref<Boolean>(false)
    const isMeeting = ref<Boolean>(false)
    const isLeave = ref<Boolean>(false)
    const isHoliday = ref<Boolean>(false)
    const isBirthday = ref<Boolean>(false)
    const event = ref<Api.Inputs.Event>()
    const birthday = ref<Api.User>()
    const vacation = ref<Api.Vacation>()
    const holiday = ref<Api.Holiday>()
    const calendar = ref<CalendarApi>()
    const dates = ref<any>()
    const selected = ref({
      events: true,
      vacations: true,
      meetings: true,
      holidays: true,
      birthdays: true
    })
    const showDialog = ref<{ [key: string]: boolean }>({})
    const meetings = ref<Api.Meetings[]>([])
    const vacations = ref<Api.Vacation[]>([])
    const holidays = ref<Api.Holiday[]>([])
    const events = ref<Api.Inputs.Event[]>([])
    const birthdays = ref<Api.User[]>([])

    function filteHome(data: any) {
      data.forEach((home: Api.Home) => {
        if (home.title === 'meeting') {
          home.meeting.forEach((meeting: Api.Meetings) => {
            meetings.value.push(meeting)
          })
        }
        if (home.title === 'birthday') {
          home.users.forEach((birthday: Api.User) => {
            let u: Api.User
            u = birthday
            u.birthday = home.date
            birthdays.value.push(u)
          })
        }
        if (home.title === 'public_holiday') {
          home.holidays.forEach((holiday: Api.Holiday) => {
            holidays.value.push(holiday)
          })
        }
        if (home.title === 'event') {
          home.event.forEach((event: Api.Inputs.Event) => {
            events.value.push(event)
          })
        }
        if (home.title === 'vacation') {
          home.vacation.forEach(async (vacation: Api.Vacation) => {
            let v: Api.Vacation
            v = vacation
            const user = await $api.users.getuser(vacation.applying_user.id, {
              disableNotify: true
            })
            v.user = user
            vacations.value.push(v)
          })
        }
      })
    }

    const homes = useAsyncState(
      () =>
        $api.home.list({
          month: currentDate.value.getMonth() + 1,
          year: currentDate.value.getFullYear()
        }),
      [],
      {
        onSuccess(data) {
          filteHome(data)
        }
      }
    )

    watch(
      () => currentDate.value,
      async (newValue, oldValue) => {
        if (
          newValue.getMonth() + 1 !== oldValue.getMonth() + 1 ||
          newValue.getFullYear() !== oldValue.getFullYear()
        ) {
          homes.execute()
        }
      }
    )

    const onSelect = async (arg: any) => {
      calendar.value = arg.view.calendar
      dates.value = arg

      openDialog(arg.startStr)
    }

    const onClick = async (arg: EventClickArg) => {
      calendar.value = arg.view.calendar

      if (arg.event.title === 'Meeting') {
        meeting.value = meetings.value.filter((meeting) => meeting.id === Number(arg.event.id))[0]
        isMeeting.value = true
        openDialog(meeting.value.id)
      } else if (arg.event.title === 'Event') {
        event.value = events.value.filter((event) => event.name === arg.event.id)[0]
        isEvent.value = true
        openDialog(event.value.name)
      } else if (arg.event.title === 'Birthday') {
        birthday.value = birthdays.value.filter(
          (birthday) => birthday.id === Number(arg.event.id)
        )[0]
        isBirthday.value = true
        openDialog(birthday.value.id)
      } else if (arg.event.title.includes('Vacation')) {
        vacation.value = vacations.value.filter(
          (vacation) => vacation.id === Number(arg.event.id)
        )[0]
        isLeave.value = true
        openDialog(vacation.value.id)
      } else if (arg.event.title === 'Public Holiday') {
        holiday.value = holidays.value.filter((holiday) => holiday.id === Number(arg.event.id))[0]
        isHoliday.value = true
        openDialog(holiday.value.id)
      }
      isViewRequest.value = true
    }

    const plugins = [dayGridPlugin, timeGridPlugin, listPlugin, interactionPlugin] as any
    const eventsOption = computed(() => {
      const normalizedMeetings = selected.value.meetings ? meetings.value.map(normalizeMeeting) : []
      const normalizedEvents = selected.value.events ? events.value.map(normalizeEvent) : []
      const normalizedBirthdays = selected.value.birthdays
        ? birthdays.value.map(normalizedBirthday)
        : []
      const normalizedHolidays = selected.value.holidays ? holidays.value.map(normalizeHoliday) : []

      const normalizedVacations = selected.value.vacations
        ? vacations.value.map(normalizeVacation)
        : []

      return [
        ...normalizedMeetings,
        ...normalizedEvents,
        ...normalizedVacations,
        ...normalizedHolidays,
        ...normalizedBirthdays
      ]
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

    const options = reactive<any>({
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
      editable: false,
      datesSet: (arg: any) => (currentDate.value = arg.view.currentStart)
    })

    function closeDialog(id: string | number) {
      isViewRequest.value, isEvent.value, isMeeting.value, (isLeave.value = false)
      event.value, meeting.value, (dates.value = undefined)
      showDialog.value[id] = false
    }

    async function createVacation(id: number | string, data: any) {
      data.vacation.forEach(async (vacation: Api.Vacation) => {
        let v: Api.Vacation
        v = vacation
        const user = await $api.users.getuser(vacation.applying_user.id, { disableNotify: true })
        v.user = user
        vacations.value.push(v)
      })
      closeDialog(id)
    }
    async function createMeeting(id: number | string, data: any) {
      data.meeting.forEach((meeting: Api.Meetings) => {
        meetings.value.push(meeting)
      })
      closeDialog(id)
    }
    async function createEvent(id: number | string, data: any) {
      data.event.forEach((event: Api.Inputs.Event) => {
        events.value.push(event)
      })

      closeDialog(id)
    }
    async function deleteVacation(id: number | string) {
      vacations.value = vacations.value.filter((vacation) => vacation.id !== id)
      closeDialog(id)
    }

    async function updateVacation(id: number | string, data: any) {
      vacations.value = vacations.value.filter((vacation) => vacation.id !== id)
      let v: Api.Vacation
      v = data
      const user = await $api.users.getuser(data.applying_user, { disableNotify: true })
      v.user = user
      v.isUpdated = true
      vacations.value.push(v)
      closeDialog(id)
    }

    async function updateVacationStatus(id: number, data: string) {
      const vacationIndex = vacations.value.findIndex((vacation) => vacation.id === id)
      if (vacationIndex !== -1) {
        if (data === 'Approve') {
          vacations.value[vacationIndex].status = 'approved'
        } else;
        if (data === 'Reject') {
          vacations.value[vacationIndex].status = 'rejected'
        }
      }
      closeDialog(id)
    }

    async function openDialog(id: string | number) {
      showDialog.value[id] = true
    }

    return {
      events,
      vacations,
      meetings,
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
      holiday,
      isHoliday,
      isBirthday,
      birthday,
      selected,
      homes,
      currentDate,
      updateVacation,
      dayCellDidMount,
      closeDialog,
      openDialog,
      onSelect,
      onClick,
      createVacation,
      createMeeting,
      createEvent,
      deleteVacation,
      updateVacationStatus,
      calenderRequest,
      meetingCard,
      eventCard,
      vacationCard,
      holidayCard,
      birthdayCard
    }
  }
}
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
</style>
