<script lang="ts">
  import type { CompanyPropertiesType } from '../../types';

  export let companies: CompanyPropertiesType[];
  /*    name: string;
  image_of: string;
  user_obj: TeamType;

  id: number;
  full_name: string;
  email: string;
  image: string;
  team: string;
  job_title: string;
  user_type: string; */
</script>

<div class="col-md-12 my-2">
  <div class="card mb-4 mb-md-0">
    <div class="card-body">
      <p class="mb-4">
        <span class="text-primary font-italic me-1"
          ><i class="bi bi-building" /></span
        >
        Companies properties
      </p>
      {#if typeof companies === 'undefined' || !Array.isArray(companies) || companies.length === 0}
        <p class="my-2 name">No companies found</p>
      {:else}
        {#each companies as company, index (index)}
          <div class="d-flex flex-row justify-content-between">
            <p class="my-2 name">
              {company.name}
            </p>
            <a
              class="btn btn-primary my-0"
              href={company.image_of + ''}
              rel="noopener noreferrer"
              target="_blank"
            >
              check company
            </a>
          </div>
        {/each}
      {/if}
    </div>
  </div>
</div>
