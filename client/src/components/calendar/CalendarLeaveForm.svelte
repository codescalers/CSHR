<script lang="ts">
  import Submit from "../submit/Submit.svelte";
  import ModalButton from "../modal/ModalButton.svelte";
  import Modal from "../modal/Modal.svelte";
  // import Input from "../input/Input.svelte";
  export let modalID = 1211112121121121;
  export let startDate: string;
  export let endDate: string;
  export let isLoading = false;
  export let isError = false;
  export let datePickerDisabled = false;
</script>

<form>
  <ModalButton label="Fill" disabled={datePickerDisabled} {modalID} />
</form>

<Modal
  title="Leave Form"
  body={"Are you sure you want to submit this form? You will not be able to edit it after submission."}
  id={modalID}
  isDelete={false}
  isDone={false}
  isFooter={true}
  doneText={"Done"}
  deleteText={"Delete"}
>
<form slot="form">
  
</form>
  <div slot="submit">
    <Submit label="Submit" onClick={() => {}} className="btn btn-primary" disabled={datePickerDisabled} />
  </div>
</Modal>
