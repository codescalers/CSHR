<script lang="ts">
    import AdminBalance from '../vacations/AdminBalance.svelte';
    import { UserStore } from '../../utils/stores';

    let user = UserStore
</script>

<div class="container">
    <AdminBalance user={$user}/>
</div>