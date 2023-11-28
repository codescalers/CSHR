<script lang="ts">
  import Vacation from "../../apis/vacations/Vacation";
  import type {
    SelectOptionsComponent,
    VacationBalanceType
  } from "../../utils/types";
  import ProfileImage from "../profile/ProfileImage.svelte";
  import Alert from "../ui/Alert.svelte";
  import Submit from "../ui/Button.svelte";
  import Input from "../ui/Input.svelte";
  import PeopleSelect from "../ui/select/UsersMultiSelect.svelte";

  let isLoading = false;
  let isUserLoaded = false;

  let isError: boolean | null = false;
  let showAlert: boolean | null = false;
  let isErrorAnunual: boolean | null,
    isErrorLeave: boolean | null,
    isErrorEmergency: boolean | null = null;

  // let userSelected: SelectOptionType[] = [];

  let isErrorUserSelected: boolean | null = null;
  let userBalance: VacationBalanceType;
  let alertMessage: string, alertType: string, alertTitle: string;
  let showLoadButton = true;

  async function loadUserBalance() {
    const userID = usersOptions.selected[0].value;
    try {
      isLoading = true;
      userBalance = await Vacation.balance(userID);
      userBalance.annual_leaves = Reflect.get(userBalance, "annual_leaves")[
        "all"
      ];
      userBalance.emergency_leaves = Reflect.get(
        userBalance,
        "emergency_leaves"
      )["all"];
      userBalance.leave_excuses = Reflect.get(userBalance, "leave_excuses")[
        "all"
      ];
      showLoadButton = false;
      isUserLoaded = true;
    } catch (err) {
      alertType = "danger";
      alertTitle = "Error while trying to get user balance";
      alertMessage = err.message;
      isError = true;
      showAlert = true;
    } finally {
      isLoading = false;
    }
  }

  $: submitDisabled =
    isErrorAnunual == true ||
    isErrorLeave == true ||
    isErrorEmergency == true ||
    usersOptions.selected!.length == 0;

  let successMessage: string;
  let errorMessage: string;

  let usersOptions: SelectOptionsComponent = {
    label: "User",
    optionsList: [],
    selected: [],
    isTop: true,
    multiple: false,
    placeholder: "Select User...",
    isError: isErrorUserSelected!
  };
</script>

<div class="bg-white card">
  <div class="card-body">
    <div class="form-outline">
      {#if !isUserLoaded}
        <PeopleSelect bind:options={usersOptions} usersInAdminOffice={true} />
      {:else if userBalance.user}
        <div class="mb-2 d-flex">
          <ProfileImage user={userBalance.user} />
          <span class="user_full_name">{userBalance.user.full_name}</span>
        </div>
        <div class="form-outline">
          <Input
            type="text"
            label={"Office location"}
            bind:value={userBalance.user.location.country}
            handleInput={() => {
              return false;
            }}
            size={25}
            errorMessage=""
            placeholder=""
            hint={""}
            disabled={true}
          />
        </div>
        <div class="form-outline">
          <Input
            type="number"
            label={"Annual leaves"}
            bind:value={userBalance.annual_leaves}
            handleInput={() => {
              return false;
            }}
            size={25}
            errorMessage="Annual leaves is invalid."
            placeholder="Annual leaves"
            hint={"Write annual leaves in numbers"}
            bind:isError={isErrorAnunual}
          />
        </div>
        <div class="form-outline">
          <Input
            type="number"
            label={"Leave execuses"}
            bind:value={userBalance.leave_excuses}
            handleInput={() => {
              return false;
            }}
            size={25}
            errorMessage="Leave execuses is invalid."
            placeholder="Leave execuses"
            hint={"Write Leave execuses in numbers"}
            bind:isError={isErrorLeave}
          />
        </div>
        <div class="form-outline">
          <Input
            type="number"
            label={"Emergency leaves"}
            bind:value={userBalance.emergency_leaves}
            handleInput={() => {
              return false;
            }}
            size={25}
            errorMessage="Emergency leaves is invalid."
            placeholder="Emergency leaves"
            hint={"Write Emergency leaves in numbers"}
            bind:isError={isErrorEmergency}
          />
        </div>
        <div class="form-check">
          <input
            class="form-check-input"
            bind:checked={userBalance.delete_old_balance}
            type="checkbox"
            value=""
            id="flexCheckDefault"
          />
          <label class="form-check-label" for="flexCheckDefault">
            Delete old balance
          </label>
        </div>
        <div class="form-outline w-100 mt-4 d-flex justify-content-end">
          <Submit
            width={"20"}
            label="Change User"
            onClick={() => (isUserLoaded = false)}
            className="abtn btn-success mr-4"
          />
          <div style="margin-left: 5px; margin-right: 5px;" />
          <Submit
            width={"30"}
            bind:successMessage
            bind:errorMessage
            label="Update Balance"
            onClick={async () => {
              isError = false;
              isLoading = true;
              try {
                Vacation.updateUserBalance(userBalance);
                successMessage =
                  "The user balance has been updated successfully.";
              } catch (error) {
                errorMessage =
                  "Error while trying to update the user balance, please check the entered data and try again.";
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
    {#if usersOptions.selected && usersOptions.selected.length > 0 && !isUserLoaded}
      <div class="mt-4 form-outline d-flex justify-content-center">
        <button
          type="button"
          class="abtn btn-success"
          on:click={loadUserBalance}
        >
          <i class="fa fa-plus" />
          Load Balance
        </button>
      </div>
    {/if}
    {#if showAlert}
      <Alert message={alertMessage} className={alertType} title={alertTitle} />
    {/if}
  </div>
</div>

<style>
  .user_full_name {
    display: flex;
    align-items: center;
    margin-left: 9px;
    font-size: 18px;
    font-weight: 600;
  }
</style>
