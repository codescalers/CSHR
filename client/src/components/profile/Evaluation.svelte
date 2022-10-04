<script lang="ts">
  import type { UserEvaluationType } from '../../types';
  import {onMount} from "svelte";
  import evaluationDataService from '../../services/axios/evaluation/EvaluationDataService';
  let evaluations: UserEvaluationType[];

  onMount(async ()=>{
    evaluations=await evaluationDataService.getByAll();
    console.log(evaluations+"sss")
  });
</script>

<div class="col-md-12 my-2">
  <div class="card mb-4 mb-md-0">
    <div class="card-body">
      <p class="mb-4">
        <span class="text-primary font-italic me-1"
          ><i class="bi bi-file-earmark-bar-graph-fill" /></span
        >
        Evaluations
      </p>

      {#if typeof evaluations === 'undefined' || !Array.isArray(evaluations) || evaluations.length === 0}
        <p class="my-2 name">No evaluations found</p>
      {:else}
        <div class="d-flex flex-row justify-content-start flex-wrap">
          {#each evaluations as evaluation, index (index)}
            <div class="p-2">
              <p class="my-2 name">
                Quarter : {evaluation.quarter}
              </p>
              <p class="my-2 name">
                Score : {evaluation.score}
              </p>
              <a
                class="btn btn-primary"
                href={evaluation.link + ''}
                rel="noopener noreferrer"
                target="_blank"
              >
                check evaluation
              </a>
            </div>
          {/each}
        </div>
      {/if}
    </div>
  </div>
</div>
