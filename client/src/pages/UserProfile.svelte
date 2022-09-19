<script lang="ts">
  import Profile from '../components/profile/Profile.svelte'
  import Sidebar from '../components/sidebar/Sidebar.svelte'
  export let isLoading = false
  export let isError: boolean | null = null
</script>

<Sidebar bind:isLoading bind:isError>
  <span slot="page-name" />
  <section class="fluid-container mt-5 content" slot="content">
    <Profile bind:isLoading bind:isError />
  </section>
</Sidebar>

<style>
  .content {
    height: fit-content;
  }
  section {
    background-color: transparent;
  }
</style>
