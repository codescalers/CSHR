<script lang="ts">
  import Sidebar from '../components/sidebar/Sidebar.svelte';
  import Calendar from '../components/calendar/Calendar.svelte';
  import CalendarEventForm from '../components/calendar/CalendarForm.svelte';
  import CalendarDetails from '../components/calendar/CalendarDetails.svelte';
  import type { eventNameType } from '../services/axios/home/types';

  let eventNames: Set<eventNameType> = new Set([
    'events',
    'vacations',
    'meetings',
    'birthdates',
  ]);
  let isLoading = false;
  let isError: boolean | null = null;
</script>

<Sidebar bind:isLoading bind:isError>
  <div slot="content">
    <div class="row">
      <div class="col-4">
        <CalendarDetails bind:eventNames bind:isLoading bind:isError />
        <CalendarEventForm />
      </div>
      <div class="col-8">
        <Calendar bind:eventNames bind:isLoading bind:isError />
      </div>
    </div>
  </div>
</Sidebar>
