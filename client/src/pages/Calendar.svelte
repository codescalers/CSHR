<script lang="ts">
  import type { UserInterface } from "../types";
  import Calendar from "../components/calendar/Calendar.svelte";
  import CalendarEventForm from "../components/calendar/CalendarForm.svelte";
  import CalendarDetails from "../components/calendar/CalendarDetails.svelte";
  export let user: UserInterface;
  import Sidebar2 from "../components/sidebar/Sidebar2.svelte";
</script>

<Sidebar2 bind:user={user}>
  <span slot="page-name">Calendar</span>
  <section class="fluid-container mt-5" slot="content">
    <div>
      <div class="d-flex flex-column-reverse align-items-sm-center flex-xl-row gap-sm-5 gap-xl-2">
        <div class="mx-5 mb-5 mb-xl-0">
          <CalendarDetails />
          <CalendarEventForm />
        </div>
        <Calendar />
      </div>
    </div>
  </section>
</Sidebar2>
