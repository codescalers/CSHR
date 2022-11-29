<script lang="ts">
  import { v4 as uuidv4 } from 'uuid';
  // headers array
  export let headers: string[];
  // table class
  export let tableClass: string = '';
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
      <slot name="table-body" />
    </table>
  </div>
</div>

<style>
  .table {
    width: 100%;
    --bs-table-striped-bg: var(--secondary-color) !important;
    --bs-table-hover-bg: var(--primary-color) !important;
    --bs-table-hover-color: rgb(0, 0, 0) !important;
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
