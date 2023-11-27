<script lang="ts">
  import { navigate } from "svelte-navigator";

  import UserDataService from "../../apis/users/users";
  import { validatePassword } from "../../utils/validations";
  import Submit from "../ui/Button.svelte";
  import Input from "../ui/Input.svelte";

  export let isLoading = false;
  export let isError = false;

  let oldPassword: string, newPassword: string;
  let isErrorOldPass: null | boolean,
    isErrorNewPass: null | boolean = null;

  $: submitDisabled =
    isErrorOldPass == true ||
    isErrorOldPass == null ||
    isErrorNewPass == true ||
    isErrorNewPass == null;

  let errorMessage: string;
  let successMessage: string;
</script>

<div class="card">
  <div class="card-body">
    <div class="row">
      <div class="col-12">
        <div class="form-outline">
          <Input
            type="password"
            label={"Old Password"}
            bind:value={oldPassword}
            handleInput={validatePassword}
            size={150}
            errorMessage="Password is invalid"
            hint={"Password must be at least 8 characters and numbers."}
            placeholder={"please enter your password here"}
            bind:isError={isErrorOldPass}
          />
        </div>
      </div>
      <div class="col-12">
        <div class="form-outline">
          <Input
            type="password"
            label={"New Password"}
            bind:value={newPassword}
            handleInput={validatePassword}
            size={150}
            errorMessage="Password is invalid"
            hint={"Password must be at least 8 characters and numbers."}
            placeholder={"please enter your password here"}
            bind:isError={isErrorNewPass}
          />
        </div>
      </div>
      <div class="col-12">
        <div class="form-outline mt-4 d-flex justify-content-center">
          <Submit
            width={"30"}
            bind:successMessage
            bind:errorMessage
            label="Submit"
            onClick={async () => {
              isLoading = true;
              try {
                await UserDataService.changePassword({
                  old_password: oldPassword,
                  new_password: newPassword
                });
                successMessage = "The password has been updated successfully.";
              } catch (error) {
                errorMessage =
                  "An error happened while trying to update the password, please check the provided data and try again.";
                isError = true;
              } finally {
                oldPassword = "";
                newPassword = "";
                isLoading = false;
                localStorage.clear();
                navigate("/login", { replace: true });
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
