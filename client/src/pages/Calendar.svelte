<script lang="ts">
  import type { UserInterface } from "../types";
  export let user: UserInterface;
  import Calendar from "../components/calendar/Calendar.svelte";
  import CalendarEventForm from "../components/calendar/CalendarForm.svelte";
  import CalendarDetails from "../components/calendar/CalendarDetails.svelte";
  import Sidebar from "../components/sidebar/Sidebar.svelte";
</script>

<Sidebar bind:user>
  <span slot="page-name">Calendar</span>
  <section class="fluid-container mt-5 content" slot="content">
    <div>
      <div
        class="d-flex flex-column-reverse align-items-sm-center flex-xl-row gap-sm-5 gap-xl-2 content"
      >
        <div class="mx-5 mb-5 mb-xl-0">
          <CalendarDetails />
          <CalendarEventForm />
        </div>
        <Calendar />
      </div>
    </div>
  </section>
</Sidebar>

<style>
  .content {
    height: fit-content;
  }
</style>
