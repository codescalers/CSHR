<script lang="ts">
  import AdminBalance from "../vacations/AdminBalance.svelte";
  export let tab: number;
</script>

<div class="container">
  <AdminBalance bind:tab />
</div>
