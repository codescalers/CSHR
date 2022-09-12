<script lang="ts">
  import CalendarBirthdayModel from "./CalendarBirthdayDataModal.svelte";
  import CalendarMeetingModel from "./CalendarMeetingDataModal.svelte";
  import CalendarEventDataModal from "./CalendarEventDataModal.svelte";
  export let item: any;
  let birthDayFlag = (item.title + "").includes("🎂");
  let meetingFlag = (item.title + "").includes("💼");
  let eventFlag = (item.title + "").includes("🎉");
  let vacationFlag = (item.title + "").includes("🌴");
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
{#if vacationFlag}{/if}
