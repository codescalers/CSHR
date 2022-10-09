<script lang="ts">
    import { Link } from 'svelte-navigator';
    import Sidebar from '../components/sidebar/Sidebar.svelte';
    export let isLoading = false;
    export let isError: boolean | null = null;
</script>
  
<Sidebar bind:isLoading bind:isError>
    <span slot="page-name" />
    <section class="fluid-container mt-5 content" slot="content">
        <Link to="/vacation/balance/">
            <p>Update vacation balance</p>
        </Link>
    </section>
</Sidebar>
