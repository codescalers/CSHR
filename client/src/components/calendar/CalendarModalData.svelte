<script lang="ts">
  import CalendarBirthdayModel from "./CalendarBirthdayDataModal.svelte";
  import CalendarMeetingModel from "./CalendarMeetingDataModal.svelte";
  export let item: any;
  let birthDayFlag = (item.title + "").includes("🎂");
  let meetingFlag = (item.title + "").includes("💼");
  let eventFlag = (item.title + "").includes("🎉");
  let vacationFlag = (item.title + "").includes("🌴");
  console.log(item);
</script>

{#if birthDayFlag}
  <CalendarBirthdayModel bind:item />
{/if}
{#if meetingFlag}
<CalendarMeetingModel bind:item />

{/if}
{#if eventFlag}{/if}
{#if vacationFlag}{/if}
