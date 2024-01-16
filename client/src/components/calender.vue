<template>
  <div class="ma-7 pa-7">
    <FullCalendar :options="options" />
  </div>

  <CustomVDialog v-if="dates?.startStr" :routeQuery="dates?.startStr" :modelValue="showDialog[dates?.startStr]">
    <v-card>
      <calenderRequest :dates="dates" />
      <v-icon class="me-2" @click.stop="closeDialog(dates?.startStr)"> mdi-eye </v-icon>
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
import CustomVDialog from '@/components/vuetify/CustomVDialog.vue'

import { ref } from "vue";

export default {
  name: "calenderCshr",
  components: {
    FullCalendar,
    CustomVDialog,
    calenderRequest,
  },


  setup() {
    const showDialog = ref<{ [key: string]: boolean }>({})
    const onSelect = async (arg: any) => {
      dates.value = arg
      console.log("onSelect", arg);
      if (dates.value) {
        console.log("here");
        openDialog(arg.startStr);
      }

    };
    const dates = ref<any>();

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
      // eventClick: onClick,
      events: [],
      editable: false,

      // datesSet: arg => (currentDate.value = arg.view.currentStart),
    });

    function closeDialog(id: string) {
      dates.value = undefined;
      showDialog.value[id] = false
    }
    async function openDialog(id: string) {
      console.log("openDialog", id);
      showDialog.value[id] = true

    }

    return {
      closeDialog,
      openDialog,
      showDialog,
      options,
      dates,
      onSelect,
      calenderRequest,
      CustomVDialog,
    };
  },
};
</script>
