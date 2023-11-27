<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import Requests from "../../apis/requests/Requests";
  import { RequestStatus } from "../../utils/enums";
  import Button from "../ui/Button.svelte";
  export let request: any;

  const dispatch = createEventDispatcher();
  let errorMessage: string | undefined;
  let successMessage: string | undefined;

  async function approveVacation(request: any) {
    successMessage = errorMessage = undefined;
    try {
      const response = await Requests.approve(request, request.id);
      successMessage = response.data.message;
      dispatch("message", {
        text: { status: RequestStatus.approved, request: request }
      });
    } catch (error: any) {
      errorMessage = error.message;
    }
  }

  async function rejectVacation(request: any) {
    successMessage = errorMessage = undefined;
    try {
      const response = await Requests.reject(request, request.id);
      successMessage = response.data.message;
      dispatch("message", {
        text: { status: RequestStatus.rejected, request: request }
      });
    } catch (error: any) {
      errorMessage = error.message;
    }
  }
</script>

<div class="row align-items-center">
  <div class="col mx-3">
    <Button
      className={"border-0 p-1 text-light btn-success btn-border btn-sm w-100 mb-1"}
      onClick={() => approveVacation(request)}
      label="Approve"
      bind:errorMessage
      bind:successMessage
    />

    <Button
      className={"border-0 p-1 text-light btn-danger btn-border btn-sm w-100"}
      onClick={() => rejectVacation(request)}
      label="Reject"
      bind:errorMessage
      bind:successMessage
    />
  </div>
</div>
