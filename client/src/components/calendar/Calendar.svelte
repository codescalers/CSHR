<script lang="ts">
  import type {
    meetingItemType,
    eventItemType,
    vacationItemType,
    birthDateItemType,
    calendarItemsType,
    eventNameType,
  } from '../../services/axios/home/types';

  import Calendar from './CalendarLayout.svelte';
  import { onMount } from 'svelte';
  import calendarDataService from '../../services/axios/home/CalendarDataService';

  export let isLoading = false;
  export let isError: boolean | null = null;
  //export let user;
  //	The Calendar Component just displays stuff in a row & column. It has no knowledge of dates.
  //	The items[] below are placed (by you) in a specified row & column of the calendar.
  //	You need to call findRowCol() to calc the rsow/col based on each items start date. Each date box has a Date() property.
  //	And, if an item overlaps rows, then you need to add a 2nd item on the subsequent row.
  let calendarItems: calendarItemsType = [];
  export let eventNames: Set<eventNameType>;

  let items: any[] | undefined;
  onMount(async () => {
    isLoading = true;
    try {
      const calendar: calendarItemsType =
        await calendarDataService.initCalendar();
      calendarItems = calendar;
      let [meetings, events, vacations, birthdates] = calendarItems;
      items = [
        ...(vacations.vacations as unknown as vacationItemType[]),
        ...(meetings.meetings as unknown as meetingItemType[]),
        ...(events.events as unknown as eventItemType[]),
        ...(birthdates.birthdates as unknown as birthDateItemType[]),
      ];
    } catch (error) {
      isError = true;
    }

    isLoading = false;
  });
  let monthNames = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
  ];

  let headers = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  let now = new Date();
  let year = now.getFullYear(); //	this is the month & year displayed
  let month = now.getMonth();
  /*   let eventText = "Click an item or date";
   */
  var days: any[] | undefined = []; //	The days to display in each box

  function initMonthItems() {
    /* 
       items = [
      {
        id: 1,
        title: "11:00 Task Early in month",
        className: "task--primary",
        description: "go to hossam office and discuss plan",
        date: new Date(y, m, randInt(6)),
        len: randInt(4) + 1,
        status: "expired",
      },
      {
        id: 2,
        title: "7:30 Wk 2 tasks",
        className: "task--warning",
        description: "go to hossam office and discuss plan",
        date: d1,
        len: randInt(4) + 2,
        status: "done",
      },
      {
        id: 3,
        title: "Overlapping Stuff (isBottom:true)",
        date: d1,
        className: "task--info",
        description: "go to hossam office and discuss plan",
        len: 4,
        isBottom: true,
        status: "undone",
      },
      {
        id: 4,
        title: "10:00 More Stuff to do",
        date: new Date(y, m, randInt(7) + 14),
        className: "task--info",
        len: randInt(4) + 1,
        description: "go to hossam office and discuss plan",
        detailHeader: "Difficult",
        detailContent: "But not especially so",
        status: "undone",
      },
      {
        id: 5,
        title: "All day task",
        date: new Date(y, m, randInt(7) + 21),
        description: "go to hossam office and discuss plan",
        className: "task--danger",
        len: 1,
        vlen: 2,
        status: "undone",
      },
      {
        id: 6,
        title: "Omars birthday",
        date: new Date(y, m, randInt(7) + 21),
        description: "Omars telegram link is: https://t.me/omar_al_sayed",
        className: "icon",
        isBottom: true,
        len: 1,
        status: "undone",
      },
    ]; */

    if (items !== undefined) {
      //This is where you calc the row/col to put each dated item

      for (let item of items) {
        let rc = findRowCol(item.date);

        if (rc == null) {
          item.startCol = item.startRow = 0;
        } else {
          item.startCol = rc.col;
          item.startRow = rc.row;
        }
      }
    }
  }

  $: items, month, year, initContent();

  // choose what date/day gets displayed in each date box.
  function initContent() {
    initMonth();
    initMonthItems();
  }

  function initMonth() {
    days = [];
    let monthAbbrev = monthNames[month].slice(0, 3);
    let nextMonthAbbrev = monthNames[(month + 1) % 12].slice(0, 3);
    //	find the last Monday of the previous month
    var firstDay = new Date(year, month, 1).getDay();
    var daysInThisMonth = new Date(year, month + 1, 0).getDate();
    var daysInLastMonth = new Date(year, month, 0).getDate();
    var prevMonth = month == 0 ? 11 : month - 1;

    //	show the days before the start of this month (disabled) - always less than 7
    for (let i = daysInLastMonth - firstDay; i < daysInLastMonth; i++) {
      let d = new Date(prevMonth == 11 ? year - 1 : year, prevMonth, i + 1);
      days.push({ name: '' + (i + 1), enabled: false, date: d });
    }
    //	show the days in this month (enabled) - always 28 - 31
    for (let i = 0; i < daysInThisMonth; i++) {
      let d = new Date(year, month, i + 1);
      if (i == 0)
        days.push({
          name: monthAbbrev + ' ' + (i + 1),
          enabled: true,
          date: d,
        });
      else days.push({ name: '' + (i + 1), enabled: true, date: d });
    }
    //	show any days to fill up the last row (disabled) - always less than 7
    for (let i = 0; days.length % 7; i++) {
      let d = new Date(month == 11 ? year + 1 : year, (month + 1) % 12, i + 1);
      if (i == 0)
        days.push({
          name: nextMonthAbbrev + ' ' + (i + 1),
          enabled: false,
          date: d,
        });
      else days.push({ name: '' + (i + 1), enabled: false, date: d });
    }
  }

  function findRowCol(dt: {
    getYear: () => any;
    getMonth: () => any;
    getDate: () => any;
  }) {
    for (let i = 0; days !== undefined && i < days.length; i++) {
      let d = days[i].date;
      if (
        d.getYear() === dt.getYear() &&
        d.getMonth() === dt.getMonth() &&
        d.getDate() === dt.getDate()
      )
        return { row: Math.floor(i / 7) + 2, col: (i % 7) + 1 };
    }
    return null;
  }

  /*   function itemClick(e) {
    eventText =
      "itemClick " + JSON.stringify(e) + " localtime=" + e.date.toString();
  }
  function dayClick(e) {
    eventText =
      "onDayClick " + JSON.stringify(e) + " localtime=" + e.date.toString();
  }
  function headerClick(e) {
    eventText = "onHheaderClick " + JSON.stringify(e);
  } */
  function next() {
    month++;
    if (month == 12) {
      year++;
      month = 0;
    }
  }
  function prev() {
    if (month == 0) {
      month = 11;
      year--;
    } else {
      month--;
    }
  }
</script>

<div class="calendar-container mx-3 my-0">
  <div class="calendar-header">
    <h1>
      <button class="icon-btn" on:click={() => prev()}>&lt;</button>
      {monthNames[month]}
      {year}
      <button class="icon-btn" on:click={() => next()}>&gt;</button>
    </h1>
  </div>

  <Calendar
    bind:eventNames
    {headers}
    {days}
    bind:items
    on:onDelete={(event) => {
      if (items != undefined) {
        items = items.filter((item) => item.id !== event.detail.id);
      } // TODO: delete from server
    }}
    on:onDone={(event) => {
      // todo update server
      if (items != undefined) {
        items = items.map((item) => {
          if (item.id === event.detail.id) {
            item.status = 'done';
          }
          return item;
        });
      }
    }}
  />
</div>

<style>
  .calendar-container {
    width: 90%;
    overflow: hidden;
    background: rgb(255 255 255);
    border: solid 0.5px rgb(43 81 95 / 19%);
    border-radius: 6px;
}
  .calendar-header {
    text-align: center;
    padding: 20px 0;
    background: #fff;
    border-bottom: 1px solid rgba(166, 168, 179, 0.12);
  }
  .calendar-header h1 {
    margin: 0;
    font-size: 18px;
    display: flex;
    align-items: center;
    justify-content: space-evenly;
  }
  .calendar-header .icon-btn {
    color: #d7e3f1;
    font-size: 1rem;
    cursor: pointer;
    background-color: rgb(43 81 95);
    font-weight: 600;
    border: #d7e3f1 1px solid;
    padding: 0.4rem 0.7rem;
    border-radius: 5px;
  }
  .calendar-header .icon-btn:hover,
  .calendar-header .icon-btn:checked {
    background-color: #2b515f;
    font-size: 1rem;
    cursor: pointer;
    color: #fff;
    font-weight: 600;
    border: #d7e3f1 1px solid;
    padding: 0.4rem 0.7rem;
    border-radius: 5px;
  }
</style>