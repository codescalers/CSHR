<script lang="ts">
  import type { CompanyPropertiesType } from '../../types';
  export let companies: CompanyPropertiesType[];
</script>

<div class="col-md-12 my-2">
  <div class="card mb-4 mb-md-0">
    <div class="card-header">
      Company properties
    </div>
    <div class="card-body">
      {#if typeof companies === 'undefined' || !Array.isArray(companies) || companies.length === 0}
        <p class="my-2 name">No companies found</p>
      {:else}
      <div class="row">
        {#each companies as company, index (index)}
          <div class="col-3">            
            <p class="my-2 name">
              {company.name}
            </p>
          </div>
          <div class="col-3 d-flex justify-content-end">
            <!-- svelte-ignore a11y-img-redundant-alt -->
            <img class="cprop"src="{process.env.APP_BASE_API_URL + company.image_of}" alt="prop image">
          </div>
        {/each}
      </div>
      {/if}
    </div>
  </div>
</div>

<style>
  .cprop{
    width: 50px;
    height: 50px;
    border-radius: 50%;
  }
</style>