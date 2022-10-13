<script lang="ts">
  import RequestModal from '../requests/requestModal.svelte';
  import Requests from "../../services/axios/requests/requests"
  import { createEventDispatcher } from 'svelte';
  import { RequestStatus } from '../../services/utils/enums';
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
			text: {"status": RequestStatus.approved, "request": request}
		});
    isRejactLoading = false;
  };

</script>

<div class="row align-items-center">
  <div class="col">
    <button
      type="button"
      on:click={() => approve_btn(request)}
      class="btn btn-success btn-border btn-sm w-100 mb-1" disabled={isApproveLoading}>
      {#if isApproveLoading}
        loading...
      {:else}
        Approve
      {/if}
    </button>
    <button
      type="button"
      on:click={() => reject_btn(request)}
      class="btn btn-danger btn-border btn-sm w-100" disabled={isRejactLoading}>
      {#if isRejactLoading}
        loading...
      {:else}
      Reject
      {/if}
      </button
    >
  </div>
  <div class="col pl-0">
    <!-- <button
      type="button"
      class="btn btn-view p-0"
      data-bs-toggle={'modal'}
      data-bs-target={'#modal'}>
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye-fill" viewBox="0 0 16 16">
        <path d="M10.5 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0z"/>
        <path d="M0 8s3-5.5 8-5.5S16 8 16 8s-3 5.5-8 5.5S0 8 0 8zm8 3.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z"/>
      </svg>
    </button> -->
    <RequestModal {request} index={request.id}/>
  </div>
</div>

<style>
  .btn-view {
    border: none !important;
  }
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