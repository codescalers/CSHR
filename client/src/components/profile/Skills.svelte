<script lang="ts">
  import type { SkillType } from '../../types';
  export let skills: SkillType[];
</script>

<div class="col-md-6">
  <div class="card mb-4 mb-md-0">
    <div class="card-body">
      <p class="mb-4">
        <span class="text-primary font-italic me-1"
          ><i class="bi bi-tools icon" /></span
        >
        Skills
      </p>
      {#if typeof skills === 'undefined' || !Array.isArray(skills) || skills.length === 0}
        <p class="my-2 name">No skills found</p>
      {:else}
        <div class="row">
          {#each skills as skill, index (index)}
            <div class="col-3 my-2 name">
              {skill.name}
            </div>
          {/each}
        </div>
      {/if}
    </div>
  </div>
</div>
