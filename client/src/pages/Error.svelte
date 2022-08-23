<script lang="ts">
  import Error404 from "../components/error/Error404.svelte";
  export let error: number;
</script>

{#if error}
  <Error404 />
{/if}
