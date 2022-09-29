<script lang="ts">
  import type { SalaryType } from '../../types';

  export let salaries: SalaryType[];
</script>

<div class="col-md-12 my-2">
  <div class="card mb-4 mb-md-0">
    <div class="card-body">
      <p class="mb-4">
        <span class="text-primary font-italic me-1"
          ><i class="bi bi-cash-coin" /></span
        >
        Salaries
      </p>
      {#if typeof salaries === 'undefined' || !Array.isArray(salaries) || salaries.length === 0}
        <p class="my-2 name">No salaries found</p>
      {:else}
        {#each salaries as salary, index (index)}
          <p class="my-2 name">{salary.Benefits}</p>
          <p class="my-2 name">{salary.current_salary}</p>
          <p class="my-2 name">{salary.joining_salary}</p>
          <p class="my-2 name">{salary.net_salary_before_joining}</p>
        {/each}
      {/if}
    </div>
  </div>
</div>
