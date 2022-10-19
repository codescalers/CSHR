<script lang="ts">
    import AdminBalance from '../vacations/AdminBalance.svelte';
    import { UserStore } from '../../stores';
    export let isLoading = false;
    export let isError: boolean | null = null;

    let user = UserStore
</script>

<div class="container">
    <AdminBalance user={$user}/>
</div>