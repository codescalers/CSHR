
<script lang="ts">
    import { UserStore } from '../../utils/stores';
    export let hint: string;
    export let header: string;
</script>

<strong>
Hey
<span class="text-primary">
    {$UserStore.full_name.length > 2 ? $UserStore.full_name : 'There'}!,
</span>
{header}
</strong>
<p class="text-muted mb-4">{hint}</p>