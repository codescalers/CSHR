<script lang="ts">
  import CalendarBirthdayModel from './CalendarBirthdayDataModal.svelte'
  import CalendarMeetingModel from './CalendarMeetingDataModal.svelte'
  import CalendarEventDataModal from './CalendarEventDataModal.svelte'
  import CalendarVacationDataModal from './CalendarVacationDataModal.svelte'
  export let item: any
  let birthDayFlag = item.eventName === 'birthdates'
  let meetingFlag = item.eventName === 'meetings'
  let eventFlag = item.eventName === 'events'
  let vacationFlag = item.eventName === 'vacations'
</script>

{#if birthDayFlag}
  <CalendarBirthdayModel bind:item />
{/if}
{#if meetingFlag}
  <CalendarMeetingModel bind:item />
{/if}
{#if eventFlag}
  <CalendarEventDataModal bind:item />
{/if}
{#if vacationFlag}
  <CalendarVacationDataModal bind:item />
{/if}
