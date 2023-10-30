<script lang="ts">
    import Submit from '../ui/Button.svelte';
    import type { SelectOptionType, UserInterface } from '../../utils/types';
    import PeopleSelect from '../ui/select/UsersMultiSelect.svelte';
    import Users from "../../apis/users/users"
    import UpdateUserProfileForm from './Forms/UpdateUserProfileForm.svelte';


    export let isLoading: boolean = false;
    export let isError: boolean = false;
    let isErrorUserSelected: boolean = false;
    
    let userSelected: SelectOptionType[] = [];
    
    let user: UserInterface;
    $: submitDisabled = userSelected.length == 0;

    async function loadUserBalance(){
        const userID = userSelected[0].value;        
        const _user: UserInterface = await Users.getUserByID(userID);
        if (_user){            
            user = _user
        }
    }

</script>

{#if !user}
    <div class="card">
        <div class="card-body">
            <div class="row">
                <PeopleSelect
                    mylabel= {"User"}
                    placeholder= {"Select User..."}
                    bind:isError={isErrorUserSelected}
                    bind:selected={userSelected}
                    isTop={true}
                    multiple={false}
                />
                <div class="col-12">
                    <div class="form-outline mt-4  d-flex justify-content-center">
                        <Submit
                            width={'25'}
                            successMessage={'Profile Updated!'}
                            errorMessage={'Profile updates failed!'}
                            label="Load user"
                            onClick={async () => {
                                isLoading = true;
                                await loadUserBalance();
                                isLoading = false;
                                
                                return isError;
                            }}
                        className=""
                        bind:disabled={submitDisabled}
                    />
                    </div>
                </div>
            </div>
        </div>
    </div>
{:else}
    <UpdateUserProfileForm user={user} />
{/if}