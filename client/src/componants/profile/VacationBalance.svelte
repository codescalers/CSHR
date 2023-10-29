<script lang="ts">
    import { onMount } from 'svelte';
    import Vacation from '../../apis/vacations/Vacation';

    export let user: any;

    type BalanceValue = {
        reserved: number;
        all: number;
    }

    interface VacationBalance {
        annual_leaves: BalanceValue;
        compensation: BalanceValue;
        emergency_leaves: BalanceValue;
        leave_excuses: BalanceValue;
        sick_leaves: BalanceValue;
        unpaid: BalanceValue;
    };

    let balance: VacationBalance;

    onMount(async () => {
        balance = await Vacation.balance(user.id);
    });

</script>

{#if balance != null}
    <div class="card">
        <div class="card-header">Vacation Balance</div>
        <div class="card-body">
            <div class="row">
                <div class="col-4 text-muted d-flex justify-content-center">Annuals</div>
                <div class="col-4 text-muted d-flex justify-content-center">Emergencies</div>
                <div class="col-4 text-muted d-flex justify-content-center">Excuses</div>
            </div>
            <div class="row">
                <div class="col-4 text-muted d-flex justify-content-center">{balance.annual_leaves.reserved} / {balance.annual_leaves.all}</div>
                <div class="col-4 text-muted d-flex justify-content-center">{balance.emergency_leaves.reserved} / {balance.emergency_leaves.all}</div>
                <div class="col-4 text-muted d-flex justify-content-center">{balance.leave_excuses.reserved} / {balance.leave_excuses.all}</div>
            </div>
        </div>
    </div>
{/if}