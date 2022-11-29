
<script lang="ts">
    import { UserStore } from '../../utils/stores';
    export let hint: string;
    export let header: string;
</script>

<strong>
Hello
<span class="text-primary">
    {$UserStore.full_name}!,
</span>
{header}
</strong>
<p class="text-muted mb-4">{hint}</p>