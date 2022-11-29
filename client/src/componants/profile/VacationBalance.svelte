<script lang="ts">
    import { onMount } from 'svelte';
    import Vacation from '../../apis/vacations/Vacation';

    export let user: any;

    let vacationBalance: any = null;
    onMount(async () => {
        vacationBalance = await Vacation.balance(user.id);
    });
</script>

{#if vacationBalance != null}
    <div class="card">
        <div class="card-header">Vacation Balance</div>
        <div class="card-body">
            <div class="row">
                <div class="col-4 text-muted d-flex justify-content-center">Annuals</div>
                <div class="col-4 text-muted d-flex justify-content-center">Emergencies</div>
                <div class="col-4 text-muted d-flex justify-content-center">Excuses</div>
            </div>
            <div class="row">
                <div class="col-4 text-muted d-flex justify-content-center">{vacationBalance.annual_leaves[0]} / {vacationBalance.annual_leaves[1]}</div>
                <div class="col-4 text-muted d-flex justify-content-center">{vacationBalance.emergency_leaves[0]} / {vacationBalance.emergency_leaves[1]}</div>
                <div class="col-4 text-muted d-flex justify-content-center">{vacationBalance.leave_excuses[0]} / {vacationBalance.leave_excuses[1]}</div>
            </div>
        </div>
    </div>
{/if}