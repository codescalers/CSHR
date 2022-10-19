<script lang="ts">
    import type { VacationBalanceType } from '../../types';
    import Input  from '../input/Input.svelte';
    import DatePickerSelect from './DatePickerSelect.svelte';
    import type {
        AdminViewInterface,
        SupervisorViewInterface,
        UserInterface,
    } from '../../types';

    export let user: AdminViewInterface | SupervisorViewInterface | UserInterface;

    const date = new Date();

    let balanceValues: VacationBalanceType = {
        "annual_leaves" : 0,
        "leave_execuses" : 0,
        "emergency_leaves" : 0,
    };

</script>

<div class="bg-white rounded-5">
    <form>
        <div class="form-outline mb-4">
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
        <div class="form-outline mb-4">
            <Input
                type="number"
                label={'Leave execuses'}
                bind:value={balanceValues.leave_execuses}
                handleInput={() => {
                    return false;
                }}
                size={25}
                errorMessage="Leave execuses is invalid."
                placeholder="Leave execuses"
                hint={'Write Leave execuses in numbers'}
            />
        </div>
        <div class="form-outline mb-4">
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
            annualValue={balanceValues.annual_leaves}
            leaveValue = {balanceValues.leave_execuses}
            emergencyValue = {balanceValues.emergency_leaves}
        />
    </form>
</div>