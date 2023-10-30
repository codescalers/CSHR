<script lang="ts">
    import Input from '../ui/Input.svelte';
    import { navigate } from 'svelte-navigator';
    import Submit from '../ui/Button.svelte';
    import { validatePassword } from '../../utils/validations';
    import UserDataService from '../../apis/users/users';

    export let isLoading: boolean = false;
    export let isError: boolean = false;

    let oldPassword: string, newPassword: string;
    let isErrorOldPass: null | boolean,
        isErrorNewPass: null | boolean
    = null;

    $: submitDisabled = 
        isErrorOldPass == true || isErrorOldPass == null ||
        isErrorNewPass == true || isErrorNewPass == null

</script>

<div class="card">
    <div class="card-body">
        <div class="row">
            <div class="col-12">
                <div class="form-outline">
                    <Input
                        type="password"
                        label={'Old Password'}
                        bind:value={ oldPassword }
                        handleInput={validatePassword}
                        size={150}
                        errorMessage="Password is invalid"
                        hint={'Password must be at least 8 characters and numbers.'}
                        placeholder={'please enter your password here'}
                        bind:isError={isErrorOldPass}
                    /> 
                </div>
            </div>
            <div class="col-12">
                <div class="form-outline">
                    <Input
                        type="password"
                        label={'New Password'}
                        bind:value={ newPassword }
                        handleInput={validatePassword}
                        size={150}
                        errorMessage="Password is invalid"
                        hint={'Password must be at least 8 characters and numbers.'}
                        placeholder={'please enter your password here'}
                        bind:isError={isErrorNewPass}
                    /> 
                </div>
            </div>
            <div class="col-12">
                <div class="form-outline mt-4 d-flex justify-content-center">
                    <Submit
                        width={'30'}
                        successMessage={'Password Updated!'}
                        errorMessage={'Password Updates Failed!'}
                        label="Submit"
                        onClick={async () => {
                            isLoading = true;
                            try {
                                await UserDataService.changePassword(
                                    {old_password: oldPassword, new_password: newPassword}
                                );
                            } catch (error) {
                                isError = true;
                            } finally {
                                oldPassword = "";
                                newPassword = "";
                                isLoading = false;
                                localStorage.clear();
                                navigate('/login', { replace: true });
                            }
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