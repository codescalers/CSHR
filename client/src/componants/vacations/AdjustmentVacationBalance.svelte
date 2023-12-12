<script lang="ts">
  import Vacation from "../../apis/vacations/Vacation";
  import { capitalize } from "../../utils/helpers";
  import { UserStore } from "../../utils/stores";
  import type {
    AvailableLeaveReason,
    VacationBalanceAdjustmentType
  } from "../../utils/types";
  import Button from "../ui/Button.svelte";
  import Input from "../ui/Input.svelte";

  let selectedReason: string;
  let value: number = 1;

  let successMessage: string | undefined;
  let errorMessage: string | undefined;

  let valueErrorMessage: string = "Value is required.";

  const reasons: AvailableLeaveReason[] = [
    "annual_leaves",
    "emergency_leaves",
    "leave_excuses"
  ];

  $: submitDisabled =
    !selectedReason ||
    value == 0 ||
    value > 30 ||
    value.toString().startsWith("0") ||
    value < 1;

  const submit = async () => {
    successMessage = undefined;
    errorMessage = undefined;

    try {
      if (submitDisabled) {
        errorMessage =
          "Please review and address any errors before submitting your request.";
        return;
      }
      const payload: VacationBalanceAdjustmentType = {
        reason: selectedReason,
        value,
        officeId: $UserStore.location.id
      };
      Vacation.vacationBalanceAdjustment(payload);
      successMessage = "The user balance has been updated successfully.";
      value = 0;
    } catch (error) {
      errorMessage =
        "Error while trying to update the user balance, please check the entered data and try again.";
    }
  };

  const validateValue = () => {
    if (!value) {
      valueErrorMessage = "Value is required.";
      return true;
    }
    if (value > 30) {
      valueErrorMessage = "The value should be lower than 30 days.";
      return true;
    }
    if (value < 1) {
      valueErrorMessage = "The value should be bigger than 1 day.";
      return true;
    }
    if (value.toString().startsWith("0")) {
      valueErrorMessage = "The value cannot start with 0.";
      return true;
    }
    return false;
  };
</script>

<div class="bg-white p-3 pt-0 mt-0 card">
  <div class="card-body">
    {#if selectedReason}
      <div>
        <small>
          <strong>Please note that </strong>
          this value will be applied to the
          <strong class="text-primary">
            {capitalize(selectedReason.replace("_", " "))}
          </strong>
          balance for all users. If you accidentally submit this form, you'll need
          to reset the value for users using the appropriate form.
        </small>
      </div>
    {/if}

    <div class="form-outline">
      <Input
        type="text"
        label={"Office location"}
        bind:value={$UserStore.location.country}
        handleInput={() => {
          return false;
        }}
        size={25}
        errorMessage="location is invalid."
        placeholder="Office location"
        hint={"This field is not editable."}
        disabled
      />
    </div>

    <div class="form-group row">
      <div class="col-4 d-flex align-items-center">
        <label for="endDayInput">Reason to be increased</label>
      </div>

      <div class="col-8 d-flex align-items-center">
        <select
          bind:value={selectedReason}
          id="Reason"
          class="form-select form-outline form-control mt-0 mv-4"
          aria-label="Default select example"
        >
          {#each Object.entries(reasons) as [index, reason]}
            <option value={reason}>
              {capitalize(reason.replace("_", " "))}
            </option>
          {/each}
        </select>
      </div>
    </div>

    <div class="form-outline">
      <Input
        type="number"
        label={"The value"}
        bind:value
        handleInput={validateValue}
        size={25}
        bind:errorMessage={valueErrorMessage}
        placeholder="This is the value to be added to all of the office members."
      />
    </div>

    <div class="form-outline w-100 mt-4 d-flex justify-content-end">
      <Button
        width={"35"}
        bind:successMessage
        bind:errorMessage
        label="Update Balance"
        onClick={submit}
        className=""
        bind:disabled={submitDisabled}
      />
    </div>
  </div>
</div>
