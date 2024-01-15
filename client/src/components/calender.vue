<script lang="ts">
import type { CalendarOptions } from "@fullcalendar/core";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction"; // Add this line
import timeGridPlugin from "@fullcalendar/timegrid";
import FullCalendar from "@fullcalendar/vue3";
import { ref } from "vue";

export default {
  name: "calenderCshr",
  components: {
    FullCalendar,
  },

  setup() {
    const vacationInfoHeaders = ["Annuals", "Emergencies", "Excuses"];
    const options = ref<CalendarOptions>({
      plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin], // Include interactionPlugin
      initialView: "dayGridMonth",
    });
    return {
      vacationInfoHeaders,
      options,
    };
  },
};
</script>
