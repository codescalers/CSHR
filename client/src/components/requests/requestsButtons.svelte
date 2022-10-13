<script lang="ts">
  import RequestModal from '../requests/requestModal.svelte';
  import updateVacations from '../../services/axios/requests/vacations';
  import updateLetters from '../../services/axios/requests/hr_letters';
  import updateCompensation from '../../services/axios/requests/compensation';
  import getRequests from '../../services/axios/requests/requests';
  export let request: any, index: number, requests: any;

  async function approve_btn(element: any, index: number) {
    document.getElementById(`approve-${index}`).style.cursor = 'wait';
    document.getElementById(`reject-${index}`).style.cursor = 'wait';
    if (element.type == 'Vacation') {
      if (await updateVacations(element.id, { status: 'approved' })) {
        document.getElementById(`approve-${index}`).style.cursor = 'defult';
        document.getElementById(`approve-${index}`).disabled = true;
        document.getElementById(`reject-${index}`).style.display = 'none';
      }
    } else if (element.type == 'HR letters') {
      document.getElementById(`approve-${index}`).style.cursor = 'wait';
      document.getElementById(`reject-${index}`).style.cursor = 'wait';
      if (await updateLetters(element.id, { status: 'approved' })) {
        document.getElementById(`approve-${index}`).style.cursor = 'defult';
        document.getElementById(`approve-${index}`).disabled = true;
        document.getElementById(`reject-${index}`).style.display = 'none';
      }
    } else if (element.type == 'Compensation') {
      document.getElementById(`approve-${index}`).style.cursor = 'wait';
      document.getElementById(`reject-${index}`).style.cursor = 'wait';
      if (await updateCompensation(element.id, { status: 'approved' })) {
        document.getElementById(`approve-${index}`).style.cursor = 'defult';
        document.getElementById(`approve-${index}`).disabled = true;
        document.getElementById(`reject-${index}`).style.display = 'none';
      }
    }
    document.body.style.cursor = 'defult';
  }
  async function reject_btn(element: any, index: number) {
    document.body.style.cursor = 'wait';
    if (element.type == 'Vacation') {
      document.getElementById(`approve-${index}`).style.cursor = 'wait';
      document.getElementById(`reject-${index}`).style.cursor = 'wait';
      if (await updateVacations(element.id, { status: 'rejected' })) {
        document.getElementById(`reject-${index}`).style.cursor = 'defult';
        document.getElementById(`reject-${index}`).disabled = true;
        document.getElementById(`approve-${index}`).style.display = 'none';
      }
    } else if (element.type == 'HR letters') {
      document.getElementById(`approve-${index}`).style.cursor = 'wait';
      document.getElementById(`reject-${index}`).style.cursor = 'wait';
      if (await updateLetters(element.id, { status: 'rejected' })) {
        document.getElementById(`reject-${index}`).style.cursor = 'defult';
        document.getElementById(`reject-${index}`).disabled = true;
        document.getElementById(`approve-${index}`).style.display = 'none';
      }
    } else if (element.type == 'Compensation') {
      document.getElementById(`approve-${index}`).style.cursor = 'wait';
      document.getElementById(`reject-${index}`).style.cursor = 'wait';
      if (await updateCompensation(element.id, { status: 'rejected' })) {
        document.getElementById(`reject-${index}`).style.cursor = 'defult';
        document.getElementById(`reject-${index}`).disabled = true;
        document.getElementById(`approve-${index}`).style.display = 'none';
      }
    }
    element = await getRequests();
    document.body.style.cursor = 'default';
  }
</script>

<div class="column">
  {#if request.status == 'Rejected' || request.status == 'rejected'}
    <div class="row align-items-center">
      <div class="col">
        <button
          type="button"
          class="btn btn-danger btn-border btn-sm w-100 "
          disabled>Rejected</button
        >
      </div>
      <div class="col pl-0">
        <button
          type="button"
          class=" btn btn-view p-0"
          data-bs-toggle={'modal'}
          data-bs-target={'#modal' + index}><i class="bi bi-eye" /></button
        >
      </div>
    </div>
  {:else if request.status == 'Approved' || request.status == 'approved'}
    <div class="row  align-items-center justify-content-start ">
      <div class="col">
        <button
          type="button"
          class="btn btn-success btn-border btn-sm w-100 "
          disabled>Approved</button
        >
      </div>
      <div class="col pl-0">
        <button
          type="button"
          class="btn  btn-view p-0"
          data-bs-toggle={'modal'}
          data-bs-target={'#modal' + index}><i class="bi bi-eye" /></button
        >
        <RequestModal {index} {request} />
      </div>
    </div>
  {:else}
    <div class="row align-items-center">
      <div class="col">
        <button
          id="approve-{index}"
          type="button"
          on:click={() => approve_btn(request, index)}
          class="btn btn-success btn-border btn-sm w-100 mb-1">Approve</button
        >
        <button
          type="button"
          id="reject-{index}"
          on:click={() => reject_btn(request, index)}
          class="btn btn-danger btn-border btn-sm w-100">Reject</button
        >
      </div>
      <div class="col pl-0">
        <button
          type="button"
          class="btn btn-view p-0"
          data-bs-toggle={'modal'}
          data-bs-target={'#modal' + index}><i class="bi bi-eye" /></button
        >
        <RequestModal {index} {request} />
      </div>
    </div>
  {/if}
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
