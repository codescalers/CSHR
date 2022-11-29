<script lang="ts">
  import Requests from "../../apis/requests/Requests"
  import { createEventDispatcher } from 'svelte';
  import { RequestStatus } from '../../utils/enums';
  export let request: any;
  const dispatch = createEventDispatcher();
  let isApproveLoading: boolean = false;
  let isRejactLoading: boolean = false;
  
  async function approve_btn(request: any){
    isApproveLoading = true;
    await Requests.approve(request, request.id);
    dispatch('message', {
			text: {"status": RequestStatus.approved, "request": request}
		});
    isApproveLoading = false;
  };
  
  async function reject_btn(request: any){
    isRejactLoading = true;
    await Requests.reject(request, request.id);
    dispatch('message', {
			text: {"status": RequestStatus.rejected, "request": request}
		});
    isRejactLoading = false;
  };

</script>

<div class="row align-items-center">
  <div class="col mx-3">
    <button
      type="button"
      on:click={() => approve_btn(request)}
      class="border-0 p-1 text-light btn-success btn-border btn-sm w-100 mb-1" disabled={isApproveLoading}>
      {#if isApproveLoading}
        loading...
      {:else}
        Approve
      {/if}
    </button>
    <button
      type="button"
      on:click={() => reject_btn(request)}
      class="border-0 p-1 text-light btn-danger btn-border btn-sm w-100" disabled={isRejactLoading}>
      {#if isRejactLoading}
        loading...
      {:else}
      Reject
      {/if}
      </button
    >
  </div>
</div>

<style>
  .btn-border {
    border-radius: 35px;
  }
  .btn-success {
    background: #29cc97;
    border-color: #29cc97;
  }
  .btn-danger {
    background: #f12b2c;
    border-color: #f12b2c;
  }
</style>