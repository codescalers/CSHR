<script lang="ts">
  import Requests from "../../services/axios/requests/requests"
  import { createEventDispatcher } from 'svelte';
  import { Link } from 'svelte-navigator';
  import { RequestStatus } from '../../services/utils/enums';
  export let request: any;
  export let showEyeButtonView: boolean = true;

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
  <div class="col">
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
  {#if showEyeButtonView}
    <div class="col pl-0">
      <Link class="text-dark" to="/{request.type.toLowerCase()}s/{request.id}">
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" class="bi bi-eye-fill" viewBox="0 0 16 16">
          <path d="M10.5 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0z"/>
          <path d="M0 8s3-5.5 8-5.5S16 8 16 8s-3 5.5-8 5.5S0 8 0 8zm8 3.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z"/>
        </svg>
      </Link>
    </div>
  {/if}
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