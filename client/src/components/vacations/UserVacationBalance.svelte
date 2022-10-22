<script lang="ts">
    import type { SelectOptionType } from '../../types';
    import PeopleSelect from '../select/PeopleSelect.svelte';
    import Alert from "../alert/Alert.svelte"
    import Submit from '../submit/Submit.svelte';
    import Input  from '../input/Input.svelte';
    import Vacation from '../../services/axios/vacations/Vacation';
    import type { VacationBalanceType } from '../../types';
    import ProfileImage from '../profile/ProfileImage.svelte';

    let isLoading: boolean = false;
    let isUserLoaded = false;

    let isError: boolean | null = false;
    let showAlert: boolean | null = false;
    let isErrorAnunual: boolean | null,
        isErrorLeave: boolean | null,
        isErrorEmergency: boolean | null
    = null;

    let userSelected: SelectOptionType[] = [];
    
    $: submitDisabled = 
        isErrorAnunual == true ||
        isErrorLeave == true ||
        isErrorEmergency == true || 
        userSelected.length == 0

    
    let isErrorUserSelected: boolean|null = null;
    let userBalance: VacationBalanceType;
    let alertMessage: string, alertType: string, alertTitle: string;
    let showLoadButton: boolean = true;

    async function loadUserBalance(){
        const userID = userSelected[0].value;
        try{
            isLoading = true;
            userBalance = await Vacation.balance(userID);
            showLoadButton = false;
        } catch (err){
            alertType = "danger";
            alertTitle = "Error while trying to get user balance"
            alertMessage = err.message;
            isLoading = false;
            isError  = true;
            showAlert  = true;
        }
        isUserLoaded = true;
    }
</script>

<div class="bg-white rounded-5">
    <div class="form-outline">
        {#if !isUserLoaded}
            <PeopleSelect
                mylabel= {"User"}
                placeholder= {"Select User..."}
                bind:isError={isErrorUserSelected}
                bind:selected={userSelected}
                isTop={true}
                multiple={false}
            />
        {:else}
            <div class="mb-2 d-flex">
                <ProfileImage user={userBalance.user}/>
                <span class="user_full_name">{userBalance.user.full_name}</span>
            </div>
            <div class="form-outline">
                <Input
                    type="number"
                    label={'Annual leaves'}
                    bind:value={userBalance.annual_leaves}
                    handleInput={() => {
                        return false;
                    }}
                    size={25}
                    errorMessage="Annual leaves is invalid."
                    placeholder="Annual leaves"
                    hint={'Write annual leaves in numbers'}
                    bind:isError={isErrorAnunual}
                />
            </div>
            <div class="form-outline">
                <Input
                    type="number"
                    label={'Leave execuses'}
                    bind:value={userBalance.leave_excuses}
                    handleInput={() => {
                        return false;
                    }}
                    size={25}
                    errorMessage="Leave execuses is invalid."
                    placeholder="Leave execuses"
                    hint={'Write Leave execuses in numbers'}
                    bind:isError={isErrorLeave}
                />
            </div>
            <div class="form-outline">
                <Input
                    type="number"
                    label={'Emergency leaves'}
                    bind:value={userBalance.emergency_leaves}
                    handleInput={() => {
                        return false;
                    }}
                    size={25}
                    errorMessage="Emergency leaves is invalid."
                    placeholder="Emergency leaves"
                    hint={'Write Emergency leaves in numbers'}
                    bind:isError={isErrorEmergency}
                />
            </div>
            <div class="form-check">
                <input class="form-check-input" 
                    bind:checked={userBalance.delete_old_balance} 
                    type="checkbox" value="" id="flexCheckDefault">
                <label class="form-check-label" for="flexCheckDefault">
                    Delete old balance
                </label>
            </div>
            <div class="form-outline mt-4  d-flex justify-content-end">
                <Submit
                    width={'15'}
                    successMessage={'User created successfully!'}
                    errorMessage={'User creation failed!'}
                    label="Submit"
                    onClick={async () => {
                        isLoading = true;
                        try {
                            Vacation.updateUserBalance(userBalance);
                        } catch (error) {
                            isError = true;
                        } finally {
                            isLoading = false;
                        }
                        return isError;
                    }}
                className=""
                bind:disabled={submitDisabled}
              />
            </div>
        {/if}
    </div>
    {#if userSelected.length > 0 && !isUserLoaded}
        <div class="mt-4 form-outline d-flex justify-content-center">
            <button type="button" class="abtn btn-success" on:click={loadUserBalance}>
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-plus-lg" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2Z"/>
                </svg>
                Load Balance
            </button>
        </div>
    {/if}
    {#if showAlert}
        <Alert message={alertMessage} type={alertType} title={alertTitle}/>
    {/if}
</div>

<style>
    .user_full_name{
        display: flex;
        align-items: center;
        margin-left: 9px;
        font-size: 18px;
        font-weight: 600;
    }
</style>