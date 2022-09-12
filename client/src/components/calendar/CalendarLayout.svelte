<script lang="ts">
  import type { eventNameType } from "../../services/axios/home/types";

  import { createEventDispatcher } from "svelte";
  import CalendarModalData from "./CalendarModalData.svelte";
  export var headers: string[] = [];
  export let days: any[] = [];
  export let items: any[] = [];
  export let eventNames: Set<eventNameType>;

  let widthItem: number;
  $: itemLetters = Math.ceil(widthItem / 14);

  let dispatch = createEventDispatcher();
  function onDelete(event: { detail: { id: any } }) {
    dispatch("onDelete", { id: event.detail.id });
  }
  function onDone(event: { detail: { id: any } }) {
    dispatch("onDone", { id: event.detail.id });
  }
</script>

<div class="calendar table-responsive">
  {#each headers as header, index (index)}
    <span class="day-name" on:click={() => dispatch("headerClick", header)}
      >{header}</span
    >
  {/each}

  {#each days as day, index (index)}
    {#if day.enabled}
      <span class="day" on:click={() => dispatch("dayClick", day)}
        >{day.name}</span
      >
    {:else}
      <span class="day day-disabled" on:click={() => dispatch("dayClick", day)}
        >{day.name}</span
      >
    {/if}
  {/each}

  {#each items as item (item.id)}
    {#if eventNames.has(item.eventName)}
      <section
        style="align-self: {item.isBottom
          ? 'end'
          : item.isStart
          ? 'start'
          : 'center'};grid-column: {item.startCol} / span {item.len};      
        grid-row: {item.startRow};  "
        on:click={() => dispatch("itemClick", item)}
        class="task {item.className} d-flex flex-column justify-content-center align-items-center"
      >
        <button
          type="button"
          class="modal-btn m-0 pl-0 "
          style="text-align: left;"
          data-bs-toggle="modal"
          data-bs-target={`#modal${item.id}`}
        >
          {item.title + ""}
        </button>

        {#if item.detailHeader}
          <div class="task-detail">
            <h2>{item.detailHeader}</h2>
            <p>{@html item.detailContent}</p>
          </div>
        {/if}
      </section>

      <!--    <Modal
      bind:title={item.title}
      bind:body={item.description}
      bind:id={item.id}
      isDelete={true}
      isDone={true}
      doneText={"Done"}
      on:onDelete={onDelete}
      on:onDone={onDone}
      deleteText={"Delete"}
      isFooter={true}
    /> -->
      <CalendarModalData
        bind:item
        on:onDelete={onDelete}
        on:onDelete={onDelete}
        on:onDone={onDone}
      />
    {/if}
  {/each}
</div>

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

  .calendar {
    display: grid;
    width: 100%;
    grid-template-columns: repeat(7, minmax(120px, 1fr));
    grid-template-rows: 50px;
    grid-auto-rows: 140px;
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
    border-left-width: 3px;
    padding: 8px 12px;
    margin: 10px;
    border-left-style: solid;
    font-size: 14px;
    position: relative;
    align-self: center;
    z-index: 2;
    border-radius: 15px;
    text-align: left;
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
  .task--danger:hover .task-detail {
    visibility: visible;
  }

  :global(.task--warning) {
    border-left-color: #fdb44d;
    background: #fef0db;
    color: #fc9b10;
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
    content: " ";
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
  .task-detail h2 {
    font-size: 15px;
    margin: 0;
    color: #91565d;
  }
  .task-detail p {
    margin-top: 4px;
    font-size: 12px;
    margin-bottom: 0;
    font-weight: 500;
    color: rgba(81, 86, 93, 0.7);
  }
</style>
