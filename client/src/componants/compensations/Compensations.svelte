<script lang="ts">
    import { onMount } from "svelte";
    import CompensationForm from "./CompensationForm.svelte";
    import CompensationList from "./CompensationList.svelte";
    import CompensationsDataService from "../../apis/compensation/compensations";
    import type { CompensationType } from "../../utils/types";

    export let isLoading: boolean = false;
    export let isError: boolean = false;

    let allUserCompensation: CompensationType[];
    onMount(async () => {
        isLoading = false;
        try {
            const response = await CompensationsDataService.userCompensations();
            allUserCompensation = response.data.results;
        } catch (error) {
            isError = true;
            throw new Error(error);
        } finally{
            isLoading = false;
        };
    });

</script>

<div class="container mt-5 pt-5">
    <div id="accordion">
        <div class="card mb-5">
            <div class="card-header" id="headingOne">
                <div class="row">
                    <div class="col-11">
                        <button class="abtn btn-link w-100 text-start" data-bs-toggle="collapse" 
                            data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne"
                            >
                            Apply for compensation days, Admin will see your request as soon as he/she can
                        </button>
                    </div>
                    <div class="col-1 d-flex justify-content-end align-items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-down-fill" viewBox="0 0 16 16">
                            <path d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/>
                        </svg>
                    </div>
                </div>
            </div>
    
            <div id="collapseOne" class="collapse show">
                <div class="card-body">
                    <CompensationForm bind:isLoading bind:isError on:message={(event)=>{
                        allUserCompensation.splice(0, 0, event.detail.postedCompensation);
                    }}/>
                </div>
            </div>
        </div>
        <div class="card">
            <div class="card-header" id="headingTwo">
                <div class="row">
                    <div class="col-11">
                        <button class="abtn btn-link collapsed w-100 text-start" data-bs-toggle="collapse" data-bs-target="#collapseTwo"
                            aria-expanded="false" aria-controls="collapseTwo">
                            List all Compensations
                        </button>
                    </div>
                    <div class="col-1 d-flex justify-content-end align-items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-down-fill" viewBox="0 0 16 16">
                            <path d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/>
                        </svg>
                    </div>
                </div>
            </div>
            <div id="collapseTwo" class="collapse">
                <div class="card-body">
                <CompensationList bind:allUserCompensation bind:isLoading bind:isError/>
                </div>
            </div>
        </div>
    </div>
</div>
