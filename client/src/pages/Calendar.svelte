<script lang="ts">
  import type { UserInterface } from "../types";
  import Calendar from "../components/calendar/Calendar.svelte";
  import CalendarEventForm from "../components/calendar/CalendarForm.svelte";
  import CalendarDetails from "../components/calendar/CalendarDetails.svelte";
  export let user: UserInterface;
</script>

<div class="fluid-container">
  <div class="d-flex gap-5">
    <div class="mx-5">
      <CalendarDetails />
      <CalendarEventForm />
    </div>

    <Calendar />
  </div>
</div>
