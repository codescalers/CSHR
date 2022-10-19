<script lang="ts">
    import { Route } from 'svelte-navigator';
    import { UserStore } from '../stores';
    import Error from './Error.svelte';
    import Sidebar from '../components/sidebar/Sidebar.svelte';
    import Tabs from "../components/dashboard/Tabs.svelte"
</script>

{#if $UserStore.user_type != "Admin"}
    <Route>
        <Error error={404} />
    </Route>
{:else}
    <Sidebar>
        <section slot="content">
            <Tabs />
        </section>
    </Sidebar>
{/if}

<style>
    .nav{
        border: none;
    }
</style>