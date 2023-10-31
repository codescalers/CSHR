
<script lang="ts">
    import { UserStore } from '../../utils/stores';
    export let hint: string;
    export let header: string;
</script>

<h4>Dashboard of <strong class="text-primary"> {$UserStore.location.country} </strong> office admins.</h4>
<hr>
<strong>
    Hey
    <span class="text-primary">
        {$UserStore.full_name.length > 2 ? $UserStore.full_name : 'There'}!,
    </span>
    {header}
</strong>
<p class="text-muted mb-4">{hint}</p>
