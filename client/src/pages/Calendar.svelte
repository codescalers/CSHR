<script lang="ts">
  import Calendar from "../componants/calendar/Calender.svelte";
  import CalendarEventsFilter from "../componants/calendar/CalendarEventsFilter.svelte";
  import CalendarEventForm from "../componants/calendar/CalendarForm.svelte";
  import { dayNames, initMonthItems, initMonth } from "../utils/calendar";
  import { findRowCol } from "../utils/calendar";
  import type { calendarItemsType, eventNameType } from "../utils/types";
  import Sidebar from "../componants/sidebar/Sidebar.svelte";
  import { UserStore } from "../utils/stores";
  import Alert from "../componants/ui/Alert.svelte";

  export let isLoading: boolean = false;

  let headers = [];
  let now = new Date();
  let year = now.getFullYear();
  let month = now.getMonth();

  var days: any[] = [];
  var items: calendarItemsType[] = [];
  let item: calendarItemsType;

  let resetVacationBalanceMessage = "";
  let oldBalanceMessage = "";

  function AdminResetBalanceNotify() {
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const lastFiveDaysOfYear = new Date(currentYear, 11, 31); // December is month 11
    lastFiveDaysOfYear.setDate(lastFiveDaysOfYear.getDate() - 4); // Last 5 days of the year

    const firstFiveDaysOfNewYear = new Date(currentYear + 1, 0, 1); // January is month 0
    firstFiveDaysOfNewYear.setDate(firstFiveDaysOfNewYear.getDate() + 4); // First 5 days of the new year

    if (
      currentDate >= lastFiveDaysOfYear &&
      currentDate <= firstFiveDaysOfNewYear
    ) {
      if ($UserStore.user_type === "Admin") {
        resetVacationBalanceMessage =
          "As we approach the end/start of the year, a friendly reminder: we're in the last/first 5 days of the year! Admins, kindly visit the dashboard to update the balance values for this year. Please note, this message will automatically vanish after the initial 5 days of the year. Thank you for your attention! 🚀📊";
      }
    }
  }

  function UserOldBalanceNotify() {
    const currentDate = new Date();

    if (currentDate.getMonth() == 2 && $UserStore.user_type !== "Admin") {
      // March is month 2
      oldBalanceMessage =
        "Just a friendly reminder: per our agreement, your balance will be automatically locked/deleted on the first day of April. Take a moment to check if you still have any remaining days on your balance and consider applying for a well-deserved vacation! 😊 Enjoy your time off! 🌴";
    }
  }

  // choose what date/day gets displayed in each date box.
  async function initContent() {
    isLoading = true;
    headers = dayNames;
    days = initMonth(days, month, year);
    items = await initMonthItems(isLoading, month, year, items, days);
    isLoading = false;
  }

  let eventNames: Set<eventNameType> = new Set([
    "event",
    "vacation",
    "meeting",
    "birthday",
    "public_holiday",
  ]);

  $: month,
    year,
    initContent(),
    AdminResetBalanceNotify(),
    UserOldBalanceNotify();
</script>

<Sidebar>
  <div slot="content">
    <div class="notifacation-hint warning-alert pt-2 pl-4 pr-4 mb-0">
      {#if resetVacationBalanceMessage.length}
        <Alert
          message={resetVacationBalanceMessage}
          className="primary"
          closable={true}
          title={`Greetings, ${$UserStore.first_name}! 🌟`}
        />
      {/if}

      {#if oldBalanceMessage.length}
        <Alert
          message={oldBalanceMessage}
          className="primary"
          closable={true}
          title={`Greetings, ${$UserStore.first_name}! 🌟`}
        />
      {/if}
    </div>
    <div class="p-4">
      <div class="row">
        <div class="col-4">
          <CalendarEventsFilter bind:eventNames />
          <CalendarEventForm
            on:message={(event) => {
              if (event.detail.postedVacation) {
                item = event.detail.postedVacation;
              }

              if (event.detail.postedMeeting) {
                item = event.detail.postedMeeting;
              }

              if (event.detail.postedEvent) {
                item = event.detail.postedEvent;
              }
              items = items;
              if (item) {
                items.push(item);
              }
              const itemDate = new Date(item.date);
              let rc = findRowCol(itemDate, days);
              if (rc == null) {
                console.log("didn`t find date for ", item);
                item.startCol = item.startRow = 0;
              } else {
                item.startCol = rc.col;
                item.startRow = rc.row;
              }
            }}
          />
        </div>
        <div class="col-8 d-flex align-center">
          <Calendar
            bind:month
            bind:year
            bind:eventNames
            bind:items
            bind:isLoading
            {headers}
            {days}
            on:onDelete={(event) => {
              if (items != undefined) {
                items = items.filter((item) => item.id !== event.detail.id);
              } // TODO: delete from server
            }}
          />
        </div>
      </div>
    </div>
  </div>
</Sidebar>
