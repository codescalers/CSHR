<script lang="ts">
    import { onMount } from 'svelte';
    import Vacation from '../../services/axios/vacations/Vacation';

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
            <div class="col-3 text-muted d-flex justify-content-center">Annuals</div>
            <div class="col-3 text-muted d-flex justify-content-center">Emergencies</div>
            <div class="col-3 text-muted d-flex justify-content-center">Excuses</div>
            <div class="col-3 text-muted d-flex justify-content-center">Public</div>
        </div>
        <div class="row">
            <div class="col-3 text-muted d-flex justify-content-center">{vacationBalance.annual_leaves}</div>
            <div class="col-3 text-muted d-flex justify-content-center">{vacationBalance.emergency_leaves}</div>
            <div class="col-3 text-muted d-flex justify-content-center">{vacationBalance.leave_excuses}</div>
            <div class="col-3 text-muted d-flex justify-content-center">{vacationBalance.public_holidays}</div>
        </div>
        </div>
    </div>
{/if}