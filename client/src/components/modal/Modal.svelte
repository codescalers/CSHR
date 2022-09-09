<script lang="ts">
  import { createEventDispatcher } from "svelte";
  export let title: string,
    id: number,
    body: string,
    isDelete: boolean,
    deleteText: string,
    isDone: boolean,
    doneText: string,
    isFooter: boolean = true;

  let dispatch = createEventDispatcher();
  function onDelete() {
    dispatch("onDelete", { id: id });
  }
  function onDone() {
    dispatch("onDone", { id: id });
  }
</script>

<div
  class="modal fade modal-lg"
  id={`modal${id}`}
  aria-labelledby="exampleModalCenterTitle"
  aria-hidden="true"
>
  <div
    class="modal-dialog model-dialog-centered model-dialog-scrollable "
    role="document"
  >
    <div class="modal-content">
      <div class="modal-header">
        {title}
        <button
          class="btn-close"
          data-bs-dismiss="modal"
          data-bs-target={`#modal${id}`}
          aria-label="Close"
        />
      </div>
      <div class="modal-body">
        {body}

        <slot name="body" />
        <slot name="form" />
      </div>
      {#if isFooter}
        <div class="modal-footer">
          {#if isDelete}
            <button
              class="btn  btn-danger"
              data-bs-dismiss="modal"
              data-bs-target="#modal"
              aria-label="Close"
              on:click={onDelete}
              >{deleteText}
              <i class="fa-solid fa-trash-can" />
            </button>
          {/if}
          {#if isDone}
            <button
              class="btn  btn-success"
              data-bs-dismiss="modal"
              data-bs-target="#modal"
              aria-label="Close"
              on:click={onDone}
              >{doneText}
              <i class="fa-solid fa-check" />
            </button>
          {/if}
          <button
            type="button"
            class="btn btn-primary"
            data-bs-dismiss="modal"
            data-bs-target="#modal"
          >
            Ok
          </button>
        </div>
      {/if}
    </div>
  </div>
</div>
