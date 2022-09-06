<script lang="ts">
  import type { UserInterface } from "../types";
  import Error404 from "../components/error/Error404.svelte";
  import Sidebar from "../components/sidebar/Sidebar.svelte";
  export let error: number;
  export let user: UserInterface;
</script>

<Sidebar bind:user>
  <span slot="page-name">Calendar</span>
  <section
    class="fluid-container  h-100 d-flex align-items-center justify-content-center"
    slot="content"
  >
    {#if error}
      <Error404 />
    {/if}
  </section>
</Sidebar>
