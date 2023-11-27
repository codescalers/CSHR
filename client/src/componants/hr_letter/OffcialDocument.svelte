<script lang="ts">
  import HRLetterDataService from "../../apis/hr_letter/hr_letter";
  import Submit from "../ui/Button.svelte";

  export let isLoading = false;
  export let isError: boolean | null = false;

  let formComment = "";
  let successMessage: string;
  let errorMessage: string;

  $: submitDisabled = formComment == "";
</script>

<div class="container mt-5 pt-5">
  <div class="card">
    <div class="card-title pt-3">
      <h5 class="text-center text-muted">
        Apply for official document, Admin will see your request as soon as
        he/she can
      </h5>
    </div>
    <div class="card-body">
      <div class="row mt-4 d-flex justify-content-center align-items-center">
        <div class="col-6">
          <div class="form-group">
            <label class="mb-2" for="exampleFormControlTextarea1"
              >Comment what is needed</label
            >
            <textarea
              class="form-control"
              bind:value={formComment}
              id="exampleFormControlTextarea1"
              rows="3"
            />
          </div>
        </div>
        <div class="col-12">
          <div class="form-outline mt-4 d-flex justify-content-center">
            <Submit
              width={"30"}
              bind:successMessage
              bind:errorMessage
              label="Submit"
              onClick={async () => {
                isLoading = true;
                try {
                  const data = { document: formComment };
                  const axios =
                    await HRLetterDataService.postOfficialDocument(data);
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
  </div>
</div>
