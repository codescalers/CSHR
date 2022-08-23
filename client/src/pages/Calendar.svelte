<script lang="ts">
  import type { UserInterface } from "../types";
  import Calendar from "../components/calendar/Calendar.svelte";
  export let user: UserInterface;
  
</script>


<div>

  calendar
  <Calendar/>
</div>