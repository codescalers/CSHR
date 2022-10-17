<script lang="ts">
    import type { EvaluationQuarter } from "../../services/utils/enums";
    import type { UserEvaluationType } from "../../types";
    export let evaluations: Array<UserEvaluationType>;
    export let quarter: EvaluationQuarter;
</script>
{#if evaluations && evaluations.length > 0}
    {#each evaluations as evaluation }
        {#if evaluation.quarter === quarter}
            <div class="card-body">
                <div class="row">
                    <div class="col-6">
                        <div class="col-3 text-muted mb-2">score</div>
                        <div class="col-3 text-primary">{evaluation.score}</div>
                    </div>
                    <div class="col-6 mb-0">
                        <div class="col-12 d-flex justify-content-end text-muted mb-2">link</div>
                        <div class="col-12 d-flex justify-content-end">
                            <a href={evaluation.link} rel="noopener noreferrer" target="_blank">
                                click to view
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        {/if}
    {/each}
{/if}