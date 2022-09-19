<script lang="ts">
  import Submit from "../submit/Submit.svelte";

  import Input from "../input/Input.svelte";
  import CalendarDataService from "../../services/axios/home/CalendarDataService";
  import { UserStore } from "../../stores";
  export let modalID = 1211112121121121;
  export let startDate: string;
  export let endDate: string;
  export let isLoading = false;
  export let isError = false;
  export let datePickerDisabled = false;

  let leaveReasonValue: string = "";
  let leaveReasonIsError: boolean | null = null;
  $: submitDisabled =
    leaveReasonIsError === null ||
    leaveReasonIsError === true ||
    datePickerDisabled;
</script>

<form>
  <Input
    type="text"
    label={"Reason"}
    bind:value={leaveReasonValue}
    handleInput={() => {
      return false;
    }}
    size={20}
    errorMessage="reason is invalid"
    hint={"please write a valid reason"}
    placeholder={"Leave Reason"}
    bind:isError={leaveReasonIsError}
  />
  <div class="my-4">
    <Submit
      label="Submit"
      successMessage="Leave Submitted "
      errorMessage="Leave Submission Failed"
      onClick={async () => {
        isLoading = true;
        try {
          await CalendarDataService.postLeave({
            end_date: endDate,
            from_date: startDate,
            reason: leaveReasonValue,
            applyingUserId: $UserStore.id,
          });
        } catch (error) {
          isError = true;
        } finally {
          isLoading = false;
          leaveReasonValue = "";
        }
        return isError;
      }}
      disabled={submitDisabled}
    />
  </div>
</form>
