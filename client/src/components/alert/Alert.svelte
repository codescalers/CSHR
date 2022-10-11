<script lang="ts">
  export let title: string, type: string, message: string;
</script>

<div class={`alert alert-${type} alert-dismissible fade show`} role="alert">
  <span>{title}</span>,{message}
  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="close" />
</div>


<style>
.alert{
  width: 100%;
}
</style>