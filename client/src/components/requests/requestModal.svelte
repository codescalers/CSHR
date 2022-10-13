<script lang="ts">
  import Modal from '../modal/Modal.svelte';
  export let index = 3;
  export let request: any;  
</script>

<Modal
  id={"this" + index}
  isDelete={false}
  isDone={false}
  isFooter={true}
  doneText={'Done'}
  deleteText={'Delete'}
  isClose={false}
>
  <header slot="header">
    <h6 class="modal-title" id="exampleModalLongTitle">
      {request.type} Details
    </h6>
  </header>
  <div slot="body">
    <div class="container d-flex flex-column gap-5 px-5 my-5">
      <div class="d-flex flex-column gap-2">
        <div class="row" style="" />
        <div class="d-flex flex-row gap-2">
          <div class="d-flex flex-column gap-1">
            <span class="text-muted">Full Name : </span>
            <span class="text-muted">Team : </span>
            <span class="text-muted">Email :</span>
            <span class="text-muted">Start Date :</span>
            <span class="text-muted">End Date :</span>
            <span class="text-muted">Reason :</span>
          </div>
          <div class="d-flex flex-column gap-1">
            <span>{request.applying_user.full_name}</span>
            <span>{request.applying_user.team}</span>
            <span>{request.applying_user.email}</span>
            <span>{request.from_date}</span>
            <span>{request.end_date}</span>
            <span>{request.reason}</span>
          </div>
        </div>
      </div>
    </div>
  </div></Modal
>
