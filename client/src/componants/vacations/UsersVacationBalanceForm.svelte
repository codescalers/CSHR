<script lang="ts">
  import Switch from "svelte-switch";

  import Vacation from "../../apis/vacations/Vacation";
  import { UserStore } from "../../utils/stores";
  import type {
    SelectOptionType,
    VacationBalanceType
  } from "../../utils/types";
  import { validateYearBalance } from "../../utils/validations";
  import ProfileImage from "../profile/ProfileImage.svelte";
  import Alert from "../ui/Alert.svelte";
  import Submit from "../ui/Button.svelte";
  import Input from "../ui/Input.svelte";
  import PeopleSelect from "../ui/select/UsersMultiSelect.svelte";

  let userIDs: number[] = [];

  let isUserLoaded: boolean = false;
  let multiple: boolean = false;
  let isErrorUserSelected: boolean;
  let userBalance: VacationBalanceType = {
    annual_leaves: 1,
    emergency_leaves: 1,
    leave_excuses: 1
  };
  let userBalances: VacationBalanceType[] = [];

  let isError: boolean | null;
  let isErrorAnunual: boolean | null;
  let isErrorLeave: boolean | null;
  let isErrorEmergency: boolean | null;

  let isLoading: boolean | null;
  let showLoadButton = true;
  let showAlert: boolean | null;

  let alertMessage: string;
  let alertType: string;
  let alertTitle: string;

  let options = {
    label: "User",
    optionsList: [],
    selected: [] as SelectOptionType[],
    isTop: true,
    multiple: multiple,
    placeholder: "Select User...",
    isError: isErrorUserSelected!
  };

  $: multiple, (options.multiple = multiple);
  $: submitDisabled =
    isErrorAnunual == true ||
    isErrorLeave == true ||
    isErrorEmergency == true ||
    options.selected!.length == 0;

  let successMessage: string;
  let errorMessage: string;

  const onLoadUsers = () => {
    if (options.selected.length > 1) {
      return setBalanceForUsers();
    } else {
      return setBalanceForUser();
    }
  };

  const setBalanceForUsers = async () => {
    // Implement logic for setting balance for multiple users
    userIDs = options.selected.map((user) => user.value);
    try {
      isLoading = true;
      userBalances = await Vacation.balance(userIDs);
      showLoadButton = false;
      isUserLoaded = true;
    } catch (err: any) {
      alertType = "danger";
      alertTitle = "Error while trying to get user balance";
      alertMessage = err.message;
      isError = true;
      showAlert = true;
    } finally {
      isLoading = false;
    }
  };

  const setBalanceForUser = async () => {
    userIDs = [options.selected![0].value];
    try {
      isLoading = true;
      userBalances = await Vacation.balance(userIDs);
      userBalance = userBalances[0];

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
    } catch (err: any) {
      alertType = "danger";
      alertTitle = "Error while trying to get user balance";
      alertMessage = err.message;
      isError = true;
      showAlert = true;
    } finally {
      isLoading = false;
    }
  };

  const updateBalance = async () => {
    isError = false;
    isLoading = true;
    try {
      const payload = {
        "annual_leaves": userBalance.annual_leaves,
        "emergency_leaves": userBalance.emergency_leaves,
        "leave_excuses": userBalance.leave_excuses,
      }
      if (submitDisabled) {
        errorMessage =
          "Please review and address any errors before submitting your request.";
        return;
      }
      await Vacation.updateUserBalance(payload, userIDs);
      successMessage = "The user balance has been updated successfully.";
    } catch (error: any) {
      errorMessage = `Error while trying to update the user balance due: "${error.message}".`;
      isError = true;
    } finally {
      isLoading = false;
    }
    return isError;
  };
</script>

<card class="bg-white card">
  <div class="card-body">
    <div class="form-outline">
      {#if !isUserLoaded}
        <div class="row">
          <div class="col-4">Update balance for multiple users</div>
          <div class="col-8">
            <Switch bind:checked={multiple} />
          </div>
        </div>
        <small>
          Note: Selected users must belong to the same office as you.
        </small>
        <PeopleSelect bind:options usersInAdminOffice={true} />
      {:else if userBalances.length}
        <div class="card profile-cards">
          {#each userBalances as balance}
            <div class="col-2">
              <ProfileImage user={balance.user} />
            </div>
          {/each}
        </div>

        <div class="form-outline">
          <Input
            type="text"
            label={"Office location"}
            bind:value={$UserStore.location.country}
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
            handleInput={validateYearBalance}
            size={25}
            errorMessage="Annual leaves is invalid."
            placeholder="Annual leaves"
            hint={"Anuual leaves should be less than 30 days."}
            bind:isError={isErrorAnunual}
          />
        </div>
        <div class="form-outline">
          <Input
            type="number"
            label={"Leave execuses"}
            bind:value={userBalance.leave_excuses}
            size={25}
            errorMessage="Leave execuses is invalid."
            placeholder="Leave execuses"
            handleInput={validateYearBalance}
            hint={"Leave execuses should be less than 30 days."}
            bind:isError={isErrorLeave}
          />
        </div>

        <div class="form-outline">
          <Input
            type="number"
            label={"Emergency leaves"}
            bind:value={userBalance.emergency_leaves}
            handleInput={validateYearBalance}
            size={25}
            errorMessage="Emergency leaves is invalid."
            placeholder="Emergency leaves"
            hint={"Emergency execuses should be less than 30 days."}
            bind:isError={isErrorEmergency}
          />
        </div>
        <!-- <div class="form-check">
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
          </div> -->
        <div class="form-outline w-100 mt-4 d-flex justify-content-end">
          <Submit
            width={"20"}
            label={options.selected.length > 1 ? "Change Users" : "Change User"}
            onClick={() => {
              isUserLoaded = false;
              userBalance = {
                annual_leaves: 1,
                emergency_leaves: 1,
                leave_excuses: 1
              };
              userBalances = [];
              options.selected = [];
              options.optionsList = [];
            }}
            className="abtn btn-success mr-4"
          />
          <div style="margin-left: 5px; margin-right: 5px;" />
          <Submit
            width={"30"}
            bind:successMessage
            bind:errorMessage
            label={options.selected.length > 1
              ? "Set Balance"
              : "Update Balance"}
            onClick={() => {
              updateBalance();
            }}
            className=""
            bind:disabled={submitDisabled}
          />
        </div>
      {/if}

      {#if options.selected && options.selected.length > 0 && !isUserLoaded}
        <div class="mt-4 form-outline d-flex justify-content-center">
          <button type="button" class="abtn btn-success" on:click={onLoadUsers}>
            <i class="fa fa-plus" />
            {options.selected.length > 1 ? "Set Balance" : "Load Balance"}
          </button>
        </div>
      {/if}
    </div>
    {#if showAlert}
      <Alert message={alertMessage} className={alertType} title={alertTitle} />
    {/if}
  </div>
</card>

<style>
  .profile-cards {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: row;
    padding: 10px;
    box-shadow: 2px 2px 14px -2px #b1b1b133;
    border-radius: 4px;
    border-color: darkseagreen;
    margin-top: 15px;
    margin-bottom: 15px;
  }
</style>
