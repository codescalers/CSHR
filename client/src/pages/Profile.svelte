<script lang="ts">
    import Profile from '../componants/profile/UserProfile.svelte';
    import Sidebar from '../componants/sidebar/Sidebar.svelte';

    export let isLoading = false;
    export let isError: boolean | null = null;
</script>
  
<Sidebar bind:isLoading bind:isError>
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
