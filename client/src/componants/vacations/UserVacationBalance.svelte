<script lang="ts">
    import type { SelectOptionType, VacationBalanceType } from '../../utils/types';
    import PeopleSelect from '../ui/select/UsersMultiSelect.svelte';
    import Alert from "../ui/Alert.svelte"
    import Submit from '../ui/Button.svelte';
    import Input  from '../ui/Input.svelte';
    import Vacation from '../../apis/vacations/Vacation';
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
        isErrorAnunual == null ||
        isErrorAnunual == true ||
        isErrorLeave == null ||
        isErrorLeave == true ||
        isErrorEmergency == true || 
        isErrorEmergency == null || 
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

<div class="bg-white p-3 card">
    <div class="card-body">
        <div class="form-outline">
            {#if !isUserLoaded}
                <PeopleSelect
                    mylabel= {"User"}
                    placeholder= {"Select User..."}
                    bind:isError={isErrorUserSelected}
                    bind:selected={userSelected}
                    isTop={true}
                    multiple={false}
                    usersInAdminOffice={true}
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
                <div class="form-outline mt-4 d-flex justify-content-end">
                    <Submit
                        width={'20'}
                        successMessage={''}
                        errorMessage={''}
                        label="Change User"
                        onClick={() => isUserLoaded = null}
                        className="abtn btn-success mr-4"
                    />

                    <Submit
                        width={'30'}
                        successMessage={'User balance updated successfully!'}
                        errorMessage={'User balance creation failed!'}
                        label="Update Balance"
                        onClick={async () => {
                            isLoading = true;
                            try {
                                Vacation.updateUserBalance(userBalance);
                                isError = false;
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
                    <i class="fa fa-plus"></i>
                    Load Balance
                </button>
            </div>
        {/if}
        {#if showAlert}
            <Alert message={alertMessage} className={alertType} title={alertTitle}/>
        {/if}
    </div>
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