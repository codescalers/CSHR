<script lang="ts">
  import type { alertType } from '../../types'
  export let title: string, type: alertType, message: string
</script>

<div class={`alert alert-${type} alert-dismissible fade show`} role="alert">
  <span>{title}</span>,{message}
  <button class="btn-close" data-bs-dismiss="alert" aria-label="close" />
</div>
