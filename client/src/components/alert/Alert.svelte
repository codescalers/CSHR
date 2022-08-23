<script lang="ts">
  type type = "success" | "info" | "warning" | "danger";
  export let title: string, type: type, message: string;
</script>

<div class={`alert alert-${type} alert-dismissible fade show`} role="alert">
  <span>{title}</span>,{message}
  <button class="btn-close" data-bs-dismiss="alert" aria-label="close" />
</div>
