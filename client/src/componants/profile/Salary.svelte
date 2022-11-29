<script lang="ts">
    import type { SalaryType } from '../../utils/types';
    export let salaries: SalaryType | null = null;    
</script>
  
<div class="col-md-12 my-2">
    <div class="card mb-4 mb-md-0">
        <div class="card-header">
            Salaries
        </div>
        <div class="card-body">
            {#if salaries === null || !salaries.current_salary || !salaries.joining_salary}
                <p class="my-2 name">No salaries found</p>
            {:else}
                <div class="row">
                    <div class="col-3 text-muted d-flex justify-content-center">Joining salary</div>
                    <div class="col-3 text-muted d-flex justify-content-center">Current salary</div>
                    <div class="col-3 text-muted d-flex justify-content-center">Net salary before joining</div>
                    <div class="col-3 text-muted d-flex justify-content-center">Benefits</div>
                </div>
                <div class="row">
                    <div class="col-3 text-muted d-flex justify-content-center">
                        <span class="mr-1">gross</span> 
                        <span class="text-primary" style="margin-left: 5px;margin-right: 5px;">
                            {salaries.joining_salary.gross}$ 
                        </span>
                        <span>net</span>
                        <span class="text-primary" style="margin-left: 5px;margin-right: 5px;">
                            {salaries.joining_salary.gross}$ 
                        </span>
                    </div>
                    <div class="col-3 text-muted d-flex justify-content-center">
                        <span class="mr-1">gross</span> 
                        <span class="text-primary" style="margin-left: 5px;margin-right: 5px;">
                            {salaries.current_salary.gross}$ 
                        </span>
                        <span>net</span>
                        <span class="text-primary" style="margin-left: 5px;margin-right: 5px;">
                            {salaries.current_salary.gross}$ 
                        </span>
                    </div>
                    <div class="col-3 text-muted d-flex justify-content-center">
                        <span class="text-primary" style="margin-left: 5px;margin-right: 5px;">
                            {salaries.net_salary_before_joining || "-"} 
                        </span> 
                    </div>
                    <div class="col-3 text-muted d-flex justify-content-center">
                        <span class="text-primary" style="margin-left: 5px;margin-right: 5px;">
                            {salaries.Benefits || "-"} 
                        </span> 
                    </div>
                </div>
            {/if}
        </div>
    </div>
</div>
  