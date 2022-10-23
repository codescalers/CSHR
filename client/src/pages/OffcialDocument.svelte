<script lang="ts">
    import OffcialDocument from '../components/hr_letter/OffcialDocument.svelte';
    import Sidebar from '../components/sidebar/Sidebar.svelte';
    export let isLoading = false;
    export let isError: boolean | null = null;
</script>
  
<Sidebar bind:isLoading bind:isError>
    <section class="fluid-container mt-5 content" slot="content">
        <OffcialDocument bind:isLoading bind:isError />
    </section>
</Sidebar>
