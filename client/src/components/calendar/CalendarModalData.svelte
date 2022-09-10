<script lang="ts">
  import Modal from "../modal/Modal.svelte";

  export let item: any;
  let birthDayFlag = (item.title + "").includes("🎂");
  let meetingFlag = (item.title + "").includes("💼");
  let eventFlag = (item.title + "").includes("🎉");
  let vacationFlag = (item.title + "").includes("🌴");
</script>

{#if birthDayFlag}
  <Modal
    bind:title={item.title}
    bind:body={item.description}
    bind:id={item.id}
    isDelete={true}
    isDone={false}
    doneText={"Done"}
    on:onDelete
    on:onDone
    deleteText={"Delete"}
    isFooter={true}
  >
    <div slot="body" >

        <div class="container d-flex flex-column gap-5 px-5 my-5 mx-xl-4">
            <div class="text-left">Details</div>
            <div class="task--danger">💼 Meeting</div>
            <div class="task--info">🎉 Event</div>
            <div class="task--warning">🌴 Vacation</div>
            <div class="task--primary">🎂 Birthday</div>
        </div>
        
    </div>
  </Modal>
{/if}
{#if meetingFlag}

{/if}
{#if eventFlag}
{/if}
{#if vacationFlag}
{/if}
