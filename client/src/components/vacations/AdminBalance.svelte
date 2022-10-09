<script lang="ts">
    import type { VacationBalanceType } from '../../types';
    import Input  from '../input/Input.svelte';
    import Error from '../../pages/Error.svelte';
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
    let isNotAdmin: boolean = false;

    if (user.user_type != "Admin"){
        isNotAdmin = true;
    }

    function handleDates(event: any){
        console.log(event.detail.text);
    }

</script>

{#if isNotAdmin}
    <!-- svelte-ignore missing-declaration -->
    <Error error={404} />
{/if}

<div class="mt-5 bg-white rounded-5 p-4">
    <strong>
        Hello
        <span class="text-primary">
            {user.full_name}
        </span>
        !, this is vacation values of 
        <span class="text-primary">
            {date.getFullYear()}
        </span>
    </strong>
    <p class="text-muted mb-4">You have to update the values every year</p>
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
        <DatePickerSelect on:message={handleDates}/>
    </form>
</div>
