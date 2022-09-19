<script lang="ts">
  import Pagination from "../pagination/Pagination.svelte";
  import { v4 as uuidv4 } from "uuid";

  // page value
  export let pageIndex: number = 1;
  // number of pages
  export let length: number = 10;
  // headers array
  export let headers: string[];
  // table class
  export let tableClass: string = "";
  // table id
  export let tableId: string = uuidv4();
</script>

<div class="container d-flex flex-column justify-content-between">
  <div class="table-responsive">
    <table
      id={tableId}
      class={`table table-striped  table-hover table-sm ${tableClass}`}
    >
      <thead class="thead-dark">
        <tr>
          <th scope="col">#</th>
          {#each headers as header, index (index)}
            <th scope="col">{header}</th>
          {/each}
        </tr>
      </thead>
      <tbody>
        <slot name="table-body" />
      </tbody>
    </table>
  </div>
  <div>
    <Pagination bind:value={pageIndex} bind:length />
  </div>
</div>

<style>
  .table {
    width: 100%;
    --bs-table-striped-bg: var(--secondary-color) !important;
    --bs-table-hover-bg: var(--primary-color) !important;
    --bs-table-hover-color: #fff !important;
  }

  .table td,
  .table th {
    padding: 0.75rem;
    vertical-align: top;
    border-top: 1px solid #dee2e6;
  }

  .table thead th {
    vertical-align: bottom;
    border-bottom: 2px solid #dee2e6;
  }

  .table tbody + tbody {
    border-top: 2px solid #dee2e6;
  }
</style>
