<script lang="ts">
  import { CalenderEventTyoe, CalenderEventEmojeTyoe } from "../../utils/enums"
  import {createEventDispatcher, onMount} from 'svelte';
  import type { calendarItemsType, eventNameType } from "../../utils/types";
  import { monthNames } from "../../utils/calendar";
  import CalendarBirthdayModel from '../ui/modals/CalendarBirthdayModel.svelte';
  import CalendarMeetingModel from '../ui/modals/CalendarMeetingModel.svelte';
  import CalendarEventDataModal from '../ui/modals/CalendarEventDataModal.svelte';
  import CalendarVacationDataModal from '../ui/modals/CalendarVacationDataModal.svelte';

  export var headers: string[] = [];
  export let days: any[] = [];
  export let items: calendarItemsType[] = [];
  export let eventNames: Set<eventNameType>;
  export let month: number;
  export let year: number;
  export let isLoading: boolean;

  let clickedItemOnModal: calendarItemsType;
  let showModal: boolean = false;
  
  let dispatch = createEventDispatcher();
 
  const capitalize = (name: string) => {
    if(name.includes("_")){
      name = name.replace("_", " ")
    }
    return name[0].toLocaleUpperCase()+name.slice(1)
  }
  const clickedItem = (item: calendarItemsType) => {    
    clickedItemOnModal = item
    showModal = true
  }
  
  let loadingBoxBg = '#F8F5F5'
  const displayLoadingBox = () => {
    if (loadingBoxBg === "#F8F5F5") {
      loadingBoxBg = "white";
    } else {
      loadingBoxBg = "#F8F5F5";
    }
  };

  onMount(() => {
    const intervalId = setInterval(() => {
      if (isLoading) {
        displayLoadingBox();
      } else {
        clearInterval(intervalId);
      }
    }, 1000);
  })

  const removeItem = () => {
    items = items.filter((item) => item !== clickedItemOnModal);
  }

  function next() {
		month++;
		if (month == 12) {
			year++;
			month=0;
		};
	};

	function prev() {
		if (month==0) {
			month=11;
			year--;
		} else {
			month--;
		};
	};
</script>

{#if isLoading}
  <div class="loading-calender mt-4">
    {#each [1,2,3,4,5,6,7] as row}
      <div class="">
        {#each [1,2,3,4,5] as col }
          <div style="background-color: {loadingBoxBg};" class="calendar-loading-box"></div>
        {/each}
      </div>
    {/each}
  </div>
{:else}
  <div class="calendar-container mx-3 my-0 mt-4">
    <div class="calendar-header">
      <h1>
        <button class="icon-btn" on:click={() => prev()}>&lt;</button>
          {monthNames[month]}
          {year}
        <button class="icon-btn" on:click={() => next()}>&gt;</button>
      </h1>
    </div>
    <div class="calendar table-responsive table-responsive">
      {#each headers as header}
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <span class="day-name" on:click={()=>dispatch('headerClick',header)}>{header}</span>
      {/each}

      {#each days as day}
        {#if day.enabled}
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <span class="day" on:click={()=>dispatch('dayClick',day)}>{day.name}</span>
        {:else}
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <span class="day day-disabled" on:click={()=>dispatch('dayClick',day)}>{day.name}</span>
        {/if}
      {/each}

      {#if items.length > 0}
        {#each items as item}
          {#if eventNames.has(item.eventName) && item.eventName === 'public_holiday'}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <section
              on:click={()=>dispatch('itemClick',item)}
              class="task event__public_holiday {item.className}"
              style="grid-column: {item.startCol} / span {item.len};      
                grid-row: {item.startRow};  
                align-self: {item.isBottom?'end':'center'};"
                >
                <button
                  type="button"
                  class="modal-btn m-0 pl-0 {item.className}"
                  on:click={() => {clickedItem(item)}}
                >
                  {capitalize(item.title)} {CalenderEventEmojeTyoe.publicHoliday}
                </button>
            </section>
          {:else if eventNames.has(item.eventName) && item.eventName === 'meeting'}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <section
              title="Click to see all meetings today!"
              on:click={()=>dispatch('itemClick',item)}
              class="task event__meeting {item.className}"
              style="grid-column: {item.startCol} / span {item.len};      
                grid-row: {item.startRow};  
                align-self: {item.isBottom?'end':'center'};"
                >
                <strong>
                  
                  <button
                    type="button"
                    class="modal-btn m-0 pl-0 {item.className}"
                    on:click={() => {clickedItem(item)}}
                  >
                    {capitalize(item.title)} {CalenderEventEmojeTyoe.meeting}
                  </button>

                </strong>
            </section>
          {:else if eventNames.has(item.eventName) && item.eventName === "vacation"}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <section
              on:click={()=>dispatch('itemClick',item)}
              class="task event__vacation {item.className}"
              style="grid-column: {item.startCol} / span {item.len};      
                grid-row: {item.startRow};  
                align-self: {item.isBottom?'end':'center'};"
                >
                <button
                  type="button"
                  class="modal-btn m-0 pl-0 {item.className}"
                  on:click={() => {clickedItem(item)}}
                >
                  {capitalize(item.title)} {CalenderEventEmojeTyoe.vacation}
                </button>
            </section>
          {:else if eventNames.has(item.eventName) && item.eventName === "event"}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <section
              on:click={()=>dispatch('itemClick',item)}
              class="task event__event {item.className}"
              style="grid-column: {item.startCol} / span {item.len};      
                grid-row: {item.startRow};  
                align-self: {item.isBottom?'end':'center'};"
                >
                <button
                  type="button"
                  class="modal-btn m-0 pl-0 {item.className}"
                  on:click={() => {clickedItem(item)}}
                >
                  {capitalize(item.title)} {CalenderEventEmojeTyoe.event}
                </button>
            </section>
            {:else if eventNames.has(item.eventName) && item.eventName === "birthday"}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <section
              on:click={()=>dispatch('itemClick',item)}
              class="task event__birthday {item.className}"
              style="grid-column: {item.startCol} / span {item.len};      
                grid-row: {item.startRow};  
                align-self: {item.isBottom?'end':'center'};"
                >
                <button
                  type="button"
                  class="modal-btn m-0 pl-0 {item.className}"
                  on:click={() => {clickedItem(item)}}
                >
                  {CalenderEventEmojeTyoe.birthday}
                </button>
            </section>
          {/if}
        {/each}
      {/if}
    </div> 
  </div>
{/if}

{#if clickedItemOnModal && clickedItemOnModal.title == CalenderEventTyoe.vacation}
  <CalendarVacationDataModal 
    bind:clickedItemOnModal 
    bind:showModal 
    currentVacationActive={clickedItemOnModal.vacation[0]}
    currentVacationID={+clickedItemOnModal.vacation[0].id}
    on:reject={removeItem}
  />
{:else if clickedItemOnModal && clickedItemOnModal.title == CalenderEventTyoe.event}
  <CalendarEventDataModal
    bind:clickedItemOnModal 
    bind:showModal
    currentEventActive={clickedItemOnModal.event[0]}
  />
{:else if clickedItemOnModal && clickedItemOnModal.title == CalenderEventTyoe.birthday}
  <CalendarBirthdayModel 
    bind:clickedItemOnModal 
    bind:showModal 
    currentUserActive={clickedItemOnModal.users[0]}
    currentUserID={clickedItemOnModal.users[0].id}
    />
{:else if clickedItemOnModal && clickedItemOnModal.title == CalenderEventTyoe.meeting}
  <CalendarMeetingModel 
    bind:showModal
    bind:clickedItemOnModal 
    currentMeetingActive={clickedItemOnModal.meeting[0]}
    currentMeetingID={clickedItemOnModal.meeting[0].id}
  />
{/if}

<style>
  .modal-btn {
    background-color: transparent;
    border: none;
    cursor: pointer;
    width: 100%;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .calendar-header h1 {
    margin: 0;
    font-size: 18px;
    display: flex;
    align-items: center;
    justify-content: space-evenly;
  }

  .calendar {
    display: grid;
    width: 100%;
    grid-template-columns: repeat(7, minmax(120px, 1fr));
    grid-template-rows: 50px;
    grid-auto-rows: 140px;
  }
  .calendar-loading-box{
    width: 130px;
    height: 140px;
    margin: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 3px;
    transition: 0.7s;
  }
  .loading-calender{
    /* width: 1200px !important; */
    overflow: hidden;
    height: 800px;
    border: 1px solid rgb(202, 199, 199);
    border-radius: 3px;
    display: flex;
    align-items: center;
    padding: 15px;
    /* justify-content: space-between; */
    background-color: #ffffffbd;
  }
  .day {
    border-bottom: 1px solid rgba(166, 168, 179, 0.12);
    border-right: 2px solid rgba(166, 168, 179, 0.12);
    text-align: left;
    padding: 14px 1.4rem;
    letter-spacing: 1px;
    font-size: 1rem;
    box-sizing: border-box;
    color: #707172;
    position: relative;
    z-index: 1;
  }
  .day:nth-of-type(7n + 7) {
    border-right: 0;
  }
  .day:nth-of-type(n + 1):nth-of-type(-n + 7) {
    grid-row: 1;
  }
  .day:nth-of-type(n + 8):nth-of-type(-n + 14) {
    grid-row: 2;
  }
  .day:nth-of-type(n + 15):nth-of-type(-n + 21) {
    grid-row: 3;
  }
  .day:nth-of-type(n + 22):nth-of-type(-n + 28) {
    grid-row: 4;
  }
  .day:nth-of-type(n + 29):nth-of-type(-n + 35) {
    grid-row: 5;
  }
  .day:nth-of-type(n + 36):nth-of-type(-n + 42) {
    grid-row: 6;
  }
  .day:nth-of-type(7n + 1) {
    grid-column: 1/1;
  }
  .day:nth-of-type(7n + 2) {
    grid-column: 2/2;
  }
  .day:nth-of-type(7n + 3) {
    grid-column: 3/3;
  }
  .day:nth-of-type(7n + 4) {
    grid-column: 4/4;
  }
  .day:nth-of-type(7n + 5) {
    grid-column: 5/5;
  }
  .day:nth-of-type(7n + 6) {
    grid-column: 6/6;
  }
  .day:nth-of-type(7n + 7) {
    grid-column: 7/7;
  }
  .day-name {
    font-size: 12px;
    text-transform: uppercase;
    color: #777;
    text-align: center;
    border-bottom: 1px solid rgba(166, 168, 179, 0.12);
    line-height: 50px;
    font-weight: 500;
  }
  .day-disabled {
    color: rgba(152, 160, 166, 0.5);
    background-color: #ffffff;
    background-image: url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23fdf9ff' fill-opacity='1' fill-rule='evenodd'%3E%3Cpath d='M0 40L40 0H20L0 20M40 40V20L20 40'/%3E%3C/g%3E%3C/svg%3E");
    cursor: not-allowed;
  }

  .task {
    z-index: 2;
    cursor: pointer;
  }
  .task:hover {
    filter: brightness(95%);
  }
  .task--danger,
  .task--info,
  .task--primary,
  .task--warning {
    font-weight: 500;
  }

  .task-detail {
    visibility: hidden;
  }

  :global(.task--warning) {
    border-left-color: #fdb44d;
    background: #fef0db;
    color: #fc9b10 !important;
    align-self: flex-start!important;
  }
  :global(.task--success) {
    border-left-color: #fef0db;
    background: #5f84d0;
    color: white !important;
    /* align-self: flex-start!important; */
    /* margin-top: 55px; */
  }
  :global(.task--danger) {
    border-left-color: #fa607e;
    grid-column: 2 / span 3;
    grid-row: 3;
    background: rgba(253, 197, 208, 0.7);
    color: #f8254e;
  }
  :global(.task--info) {
    background: rgba(192, 191, 191, 0.7);
    color: #444;
  }
  :global(.task--primary) {
    background: #c0d6ff;
    color: #0a5eff;
  }

  :global(.task-detail) {
    position: absolute;
    left: 0;
    top: calc(100% + 8px);
    background: #efe;
    border: 1px solid rgba(166, 168, 179, 0.2);
    color: #100;
    padding: 20px;
    box-sizing: border-box;
    border-radius: 14px;
    box-shadow: 0 4px 4px rgba(0, 0, 0, 0.08);
    z-index: 1000;
  }
  .task-detail:after,
  .task-detail:before {
    bottom: 100%;
    left: 30%;
    border: solid transparent;
    content: ' ';
    height: 0;
    width: 0;
    position: absolute;
    pointer-events: none;
  }
  .task-detail:before {
    border-bottom-color: rgba(166, 168, 179, 0.2);
    border-width: 8px;
    margin-left: -8px;
  }
  .task-detail:after {
    border-bottom-color: #fff;
    border-width: 6px;
    margin-left: -6px;
  }
  .calendar-container {
    width: 100%;
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