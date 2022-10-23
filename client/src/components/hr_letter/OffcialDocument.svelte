<script lang="ts">
    import Submit from '../submit/Submit.svelte';
    import HRLetterDataService from "../../services/axios/hr_letter/hr_letter"

    export let isLoading: boolean = false;
    export let isError: boolean = false;

    let formComment: string;
    let successMessage: string;
    let errorMessage: string;  

    $: submitDisabled = formComment == ""
</script>

<h5 class="text-center text-muted">Apply for official document, Admin will see your request as soon as he/she can</h5>

<div class="container">
    <div class="row mt-4 d-flex justify-content-center align-items-center">
        <div class="col-6">
            <div class="form-group">
                <label class="mb-4" for="exampleFormControlTextarea1">Comment what is needed</label>
                <textarea class="form-control" bind:value={formComment} id="exampleFormControlTextarea1" rows="3"></textarea>
            </div>
        </div>
        <div class="col-12">
            <div class="form-outline mt-4 d-flex justify-content-center">
                <Submit
                    width={'30'}
                    successMessage={successMessage}
                    errorMessage={errorMessage}
                    label="Submit"
                    onClick={async () => {
                        isLoading = true;
                        try {
                            const data = {"document": formComment}
                            const axios = await HRLetterDataService.postOfficialDocument(data);
                            isError = false;
                            successMessage = axios.data.message;
                        } catch (error) {
                            isError = true;
                            errorMessage = error.message;
                        } finally {
                            formComment = "";
                            isLoading = false;
                        }
                        return isError;
                    }}
                className=""
                bind:disabled={submitDisabled}
            />
            </div>
        </div>
    </div>
</div>