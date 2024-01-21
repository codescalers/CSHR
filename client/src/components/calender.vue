<template>
  <div class="ma-7 pa-7">
    <FullCalendar :options="options" />
  </div>

  <CustomVDialog v-if="dates?.startStr" :routeQuery="dates?.startStr" :modelValue="showDialog[dates?.startStr]">
    <v-card>
      <calenderRequest :dates="dates" @close-dialog="closeDialog(dates?.startStr)" />
    </v-card>
  </CustomVDialog>


  <CustomVDialog v-if="isViewRequest && isMeeting && meeting" :routeQuery="meeting.id"
    :modelValue="showDialog[meeting.id]">
    <v-card>
      <meetingCard :meeting="meeting" @close-dialog="closeDialog(meeting.id)" />
    </v-card>

  </CustomVDialog>

  <CustomVDialog v-if="isViewRequest && isEvent && event" :routeQuery="event.name" :modelValue="showDialog[event.name]">
    <v-card>
      <eventCard :event="event" @close-dialog="closeDialog(event.name)" />
    </v-card>
  </CustomVDialog>

  <CustomVDialog v-if="isViewRequest && isLeave && vacation" :routeQuery="vacation.id"
    :modelValue="showDialog[vacation.id]">
    <v-card>
      <vacationCard :vacation="vacation" @close-dialog="closeDialog(vacation.id)" />
    </v-card>
  </CustomVDialog>
</template>
<script lang="ts">
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction"; // Add this line
import timeGridPlugin from "@fullcalendar/timegrid";
import FullCalendar from "@fullcalendar/vue3";
import listPlugin from '@fullcalendar/list';
import calenderRequest from "@/components/calenderRequest.vue";
import CustomVDialog from '@/components/vuetify/CustomVDialog.vue';
import meetingCard from '@/components/cards/meetingCard.vue';
import eventCard from '@/components/cards/eventCard.vue';
import vacationCard from '@/components/cards/vacationCard.vue';


import { onMounted, ref } from "vue";
import type { Api } from "@/types";
import { $api } from "@/clients";
import type { EventClickArg } from "@fullcalendar/core/index.js";
import type { CalendarApi } from "@fullcalendar/core/index.js";

export default {
  name: "calenderCshr",
  components: {
    FullCalendar,
    CustomVDialog,
    calenderRequest,
    meetingCard,
    eventCard,
    vacationCard,
  },


  setup() {
    const meetings = ref<Api.Meetings[]>([]);
    const meeting = ref<Api.Meetings>();
    const isViewRequest = ref<Boolean>(false);
    const isEvent = ref<Boolean>(false);
    const isMeeting = ref<Boolean>(false);
    const isLeave = ref<Boolean>(false);
    const events = ref<Api.Inputs.Event[]>([]);
    const event = ref<Api.Inputs.Event>();

    const vacations = ref<Api.Vacation[]>([]);
    const vacation = ref<Api.Vacation>();
    const calendar = ref<CalendarApi>();


    const dates = ref<any>();
    const showDialog = ref<{ [key: string]: boolean }>({})
    const onSelect = async (arg: any) => {
      calendar.value = arg.view.calendar;
      dates.value = arg

      const validated: boolean = validateDate(arg.start);
      if (validated) {
        if (dates.value) {
          openDialog(arg.startStr);
        }
      } else {
        calendar.value?.unselect();
      }

    };

    const validateDate = (startDate: Date) => {
      const today = new Date();
      today.setHours(0, 0, 0, 0); // Set the time to midnight for accurate comparison

      if (startDate < today) {
        console.error("Start date cannot be in the past.");
        return false;
      }

      return true;
    };

    const onClick = async (arg: EventClickArg) => {
      calendar.value = arg.view.calendar;

      if (arg.event.title === "Meeting") {

        meeting.value = meetings.value.filter(meeting => meeting.id === Number(arg.event.id))[0];
        isMeeting.value = true;
        openDialog(meeting.value.id);

      } else if (arg.event.title === "Event") {

        event.value = events.value.filter(event => event.name === arg.event.id)[0];
        isEvent.value = true;
        openDialog(event.value.name);
      }
      else if (arg.event.title === "Vacation") {

        vacation.value = vacations.value.filter(vacation => vacation.id === Number(arg.event.id))[0];
        isLeave.value = true;
        openDialog(vacation.value.id);

      }
      isViewRequest.value = true;
    };


    const options = ref<any>({
      plugins: [dayGridPlugin, timeGridPlugin, listPlugin, interactionPlugin],
      dayMaxEvents: true,
      initialView: 'dayGridMonth',
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,dayGridWeek,listDay',
      },
      selectable: true,
      weekends: true,
      select: onSelect,
      eventClick: onClick,
      events: [],
      editable: false,

    });

    async function getMeetings() {
      meetings.value = await $api.meeting.list();
      for (const meeting of meetings.value) {
        pushMeeting(meeting);
      }
    }
    async function getEvents() {
      events.value = await $api.event.list();
      for (const event of events.value) {
        pushEvent(event);
      }
    }

    async function getVacations() {
      vacations.value = await $api.vacations.list();
      for (const vacation of vacations.value) {
        pushVacation(vacation);
      }
    }
    onMounted(async () => {
      await getMeetings();
      await getEvents();
      await getVacations();
    })
    const handelDates = (dates: any): any => {
      const endDate = new Date(dates.end || '');
      if (dates.cut) {
        endDate.setDate(endDate.getDate() - 1);
      } else if (dates.add) {
        endDate.setDate(endDate.getDate() + 1);
      }

      dates.end = endDate;
      dates.start = new Date(dates.start);

      const endStr = `${endDate.getFullYear()}-${endDate.getMonth() + 1}-${endDate.getDate()}`;
      const startStr = `${dates.start.getFullYear()}-${dates.start.getMonth() + 1}-${dates.start.getDate()}`;

      dates.endStr = endStr;
      dates.startStr = startStr;
      return dates;
    };

    const pushVacation = (v: Api.Vacation) => {
      const dates = handelDates({
        end: v.end_date,
        start: v.from_date,
        add: true,
      });

      const vacation = {
        title: "Vacation",
        color: "primary",
        start: dates.start,
        end: dates.end,
        backgroundColor: "primary",
        id: v.id,
        allDay: true,
      };
      options.value.events = [...(options.value.events as []), vacation];
    };

    const pushEvent = (e: Api.Inputs.Event) => {
      const dates = handelDates({
        end: e.end_date,
        start: e.from_date,
        add: true,
      });

      const event = {
        title: "Event",
        color: "primary",
        start: dates.start,
        end: dates.end,
        backgroundColor: "primary",
        id: e.name,
        allDay: true,
      };
      options.value.events = [...(options.value.events as []), event];
    };

    const pushMeeting = (m: Api.Meetings) => {
      const dates = handelDates({
        end: m.date,
        start: m.date,
        add: true,
      });

      const meeting = {
        title: "Meeting",
        color: "secondary",
        start: dates.start,
        end: dates.end,
        backgroundColor: "secondary",
        id: m.id,
        allDay: true,
      };
      options.value.events = [...(options.value.events as []), meeting];
    };
    function closeDialog(id: string | number) {
      isViewRequest.value, isEvent.value, isMeeting.value, isLeave.value = false;
      event.value, meeting.value, dates.value = undefined;
      showDialog.value[id] = false
    }

    async function openDialog(id: string | number) {
      showDialog.value[id] = true
    }



    return {
      isViewRequest,
      isEvent,
      isLeave,
      isMeeting,
      meeting,
      event,
      showDialog,
      options,
      dates,
      vacation,
      closeDialog,
      openDialog,
      onSelect,
      onClick,
      calenderRequest,
      CustomVDialog,
      meetingCard,
      eventCard,
      vacationCard,
    };
  },
};
</script>
