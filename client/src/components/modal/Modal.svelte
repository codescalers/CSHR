<script lang="ts">
  export let title: string, description: string, footer: string;
</script>

<div
  class="modal fade modal-lg"
  id={`modal`}
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
          data-bs-target="#modal"
          aria-label="Close"
        />
      </div>
      <div class="modal-body">{description}</div>
      <div class="modal-footer">{footer}</div>
    </div>
  </div>
</div>
