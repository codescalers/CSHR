<script lang="ts">
  import { onMount } from "svelte";

  import Evaluation from "../../apis/evaluation/Evaluation";
  import { EvaluationQuarter } from "../../utils/enums";
  import type { UserEvaluationType } from "../../utils/types";
  import Quarter from "./EvaluationQuarter.svelte";
  export let user: any;

  let evaluations: UserEvaluationType[];
  let date: Date = new Date();
  let year: number = date.getFullYear();
  let isLoading = false;

  async function plusOneYear() {
    isLoading = true;
    year += 1;
    await filterUserEvaluationBaedOnYear(year);
    isLoading = false;
  }

  async function minusOneYear() {
    isLoading = true;
    year -= 1;
    await filterUserEvaluationBaedOnYear(year);
    isLoading = false;
  }
  async function filterUserEvaluationBaedOnYear(year: number) {
    evaluations = await Evaluation.UserEvaluations(user.id, year);
  }

  onMount(async () => {
    isLoading = true;
    evaluations = await Evaluation.UserEvaluations(user.id, year);
    isLoading = false;
  });

  // EvaluationQuarter
</script>

<div class="col-md-12 my-2">
  <div class="card mb-4 mb-md-0">
    <div class="card-header">Evaluations</div>
    <div class="card-body">
      <div class="row">
        <div class="col-2">
          <button
            class="c-btn d-flex justify-content-center align-items-center"
            on:click={minusOneYear}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              fill="currentColor"
              class="bi bi-caret-left-fill"
              viewBox="0 0 16 16"
            >
              <path
                d="m3.86 8.753 5.482 4.796c.646.566 1.658.106 1.658-.753V3.204a1 1 0 0 0-1.659-.753l-5.48 4.796a1 1 0 0 0 0 1.506z"
              />
            </svg>
          </button>
        </div>
        <div class="col-8 d-flex justify-content-center align-items-center">
          <p class="text-center text-muted year">{year}</p>
        </div>
        <div class="col-2">
          <button
            class="c-btn justify-content-center align-items-center"
            on:click={plusOneYear}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              fill="currentColor"
              class="bi bi-caret-right-fill"
              viewBox="0 0 16 16"
            >
              <path
                d="m12.14 8.753-5.482 4.796c-.646.566-1.658.106-1.658-.753V3.204a1 1 0 0 1 1.659-.753l5.48 4.796a1 1 0 0 1 0 1.506z"
              />
            </svg>
          </button>
        </div>
      </div>
      {#if isLoading}
        <div class="d-flex justify-content-center align-items-center">
          <div class="spinner-grow" role="status">
            <span class="sr-only">Loading...</span>
          </div>
        </div>
      {:else}
        <div class="mt-2 card-header b-none text-center text-muted">
          <strong>{EvaluationQuarter.JAN_MARCH}</strong>
        </div>
        <Quarter quarter={EvaluationQuarter.JAN_MARCH} {evaluations} />
        <div class="mt-2 card-header b-none text-center text-muted">
          <strong>{EvaluationQuarter.APR_JUN}</strong>
        </div>
        <Quarter quarter={EvaluationQuarter.APR_JUN} {evaluations} />
        <div class="mt-2 card-header b-none text-center text-muted">
          <strong>{EvaluationQuarter.JUL_SEP}</strong>
        </div>
        <Quarter quarter={EvaluationQuarter.JUL_SEP} {evaluations} />
        <div class="mt-2 card-header b-none text-center text-muted">
          <strong>{EvaluationQuarter.OCT_DEC}</strong>
        </div>
        <Quarter quarter={EvaluationQuarter.OCT_DEC} {evaluations} />
      {/if}
    </div>
  </div>
</div>

<style>
  .year {
    font-size: 21px;
    font-weight: 700;
    margin: 0;
  }
  .c-btn {
    height: 42px;
    max-height: 42px;
    width: 45px;
    max-width: 45px;
    min-width: 45px;
    padding: 0;
    margin: 0;
    background: rgb(0 0 0 / 0%);
    border: none;
    outline: none;
  }
</style>
