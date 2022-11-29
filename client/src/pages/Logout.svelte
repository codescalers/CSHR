<script lang="ts">
    import { navigate } from 'svelte-navigator';

    localStorage.removeItem("accesstoken");
    localStorage.removeItem("refreshtoken");
    navigate('/login', { replace: true });
</script>
