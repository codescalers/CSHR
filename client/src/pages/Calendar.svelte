<script lang="ts">
  import type { UserInterface } from "../types";
  import Calendar from "../components/calendar/Calendar.svelte";
import Sidebar from "../components/sidebar/sidebar.svelte";
  export let user: UserInterface;
  
</script>


<div>
  
  <Sidebar/>
  <Calendar/>
  
</div>