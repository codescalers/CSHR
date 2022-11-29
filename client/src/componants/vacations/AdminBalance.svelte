<script lang="ts">
    import type { VacationBalanceType } from '../../utils/types';
    import Input  from '../ui/Input.svelte';
    import DatePickerSelect from './DatePickerSelect.svelte';
    import { UserStore } from "../../utils/stores"

    let balanceValues: VacationBalanceType = {
        "user": $UserStore,
        "annual_leaves": 0,
        "leave_excuses": 0,
        "emergency_leaves": 0,
        delete_old_balance: false
    };

    const removeValues = (event: { detail: {
      emergencyValue: any;
      leaveValue: any; annualValue: number; }; 
    }) => {
        balanceValues.annual_leaves = event.detail.annualValue
        balanceValues.leave_excuses = event.detail.leaveValue
        balanceValues.emergency_leaves = event.detail.emergencyValue
    }

</script>

<div class="bg-white p-3 card">
    <div class="card-body">
        <div class="form-outline">
            <Input
                type="number"
                label={'Annual leaves'}
                bind:value={balanceValues.annual_leaves}
                handleInput={() => {
                    return false;
                }}
                size={25}
                errorMessage="Annual leaves is invalid."
                placeholder="Annual leaves"
                hint={'Write annual leaves in numbers'}
            />
        </div>
        <div class="form-outline">
            <Input
                type="number"
                label={'Leave execuses'}
                bind:value={balanceValues.leave_excuses}
                handleInput={() => {
                    return false;
                }}
                size={25}
                errorMessage="Leave execuses is invalid."
                placeholder="Leave execuses"
                hint={'Write Leave execuses in numbers'}
            />
        </div>
        <div class="form-outline">
            <Input
                type="number"
                label={'Emergency leaves'}
                bind:value={balanceValues.emergency_leaves}
                handleInput={() => {
                    return false;
                }}
                size={25}
                errorMessage="Emergency leaves is invalid."
                placeholder="Emergency leaves"
                hint={'Write Emergency leaves in numbers'}
            />
        </div>
        <DatePickerSelect
            on:message={removeValues}
            annualValue={balanceValues.annual_leaves}
            leaveValue = {balanceValues.leave_excuses}
            emergencyValue = {balanceValues.emergency_leaves}
        />
    </div>
</div>