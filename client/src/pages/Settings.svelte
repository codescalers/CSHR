<script lang="ts">
    import Settings from '../componants/settings/Settings.svelte';
    import Sidebar from '../componants/sidebar/Sidebar.svelte';
</script>

<Sidebar>
    <section slot="content">
        <Settings />
    </section>
</Sidebar>