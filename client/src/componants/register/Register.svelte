<script lang="ts">
  import RegisterDataService from "../../apis/users/users";
  import {
    GenderChoice,
    TeamChoice,
    UserTypeChoice
  } from "../../utils/choices";
  import { clearUserData } from "../../utils/helpers";
  import registeringDataType from "../../utils/registeringData";
  import type {
    registeringData,
    SelectOptionsComponent
  } from "../../utils/types";
  import {
    // validateSalary,
    validateBirthday,
    validateEmail,
    validateName,
    validatePassword,
    validatePhoneNumber,
    validateSpcialEmptyString,
    validateTelegramLink
  } from "../../utils/validations";
  import Submit from "../ui/Button.svelte";
  import Input from "../ui/Input.svelte";
  import LocationSelect from "../ui/select/LocationSelect.svelte";
  import MultiSelect from "../ui/select/MultiSelect.svelte";
  import SelectImage from "../ui/select/SelectImage.svelte";
  import PeopleSelect from "../ui/select/UsersMultiSelect.svelte";

  export let isLoading = false;
  export let isError = false;

  let image: HTMLImageElement;
  let imageSrc: string;
  let registeration: registeringData = registeringDataType;

  let isErrorfName: null | boolean,
    isErrorlName: null | boolean,
    isErrormail: null | boolean,
    isErrorMobile: null | boolean,
    isErrorJobTitle: null | boolean,
    isErrorpass: null | boolean,
    isErrorLink: null | boolean,
    // isErrorBenefits: null | boolean,
    isErrorBirthday: null | boolean,
    isErrorJoiningDate: null | boolean,
    // isErrorLocation: null | boolean,
    // isErrorSuperuser: null | boolean,
    isErrorCurrentNetSalary: null | boolean,
    isErrorCurrentGrossSalary: null | boolean,
    // isErrorNetJoinningSalary: null | boolean,
    // isErrorGrossJoinningSalary: null | boolean,
    // isErrorNetBeforeJoinningSalary: null | boolean,
    isErrorSocialNumber: null | boolean,
    isErrorAddress: null | boolean = null;

  $: submitDisabled =
    isErrorCurrentGrossSalary == true ||
    isErrorCurrentNetSalary == true ||
    isErrorBirthday == true ||
    isErrorJoiningDate == true ||
    isErrorLink == true ||
    isErrorpass == true ||
    isErrorJobTitle == true ||
    isErrorMobile == true ||
    isErrormail == true ||
    isErrorSocialNumber == true ||
    isErrorlName == true ||
    isErrorfName == true ||
    isErrorAddress == true ||
    isErrorAddress == null ||
    locationOptions.selected!.length == 0 ||
    departmentOptions.selected!.length == 0 ||
    genderOptions.selected!.length == 0 ||
    userTypeOptions.selected!.length == 0 ||
    registeration.job_title.trim().length < 3 ||
    registeration.social_insurance_number.trim().length < 3 ||
    !registeration.address.trim().length;

  // let teamSelectOptions: SelectOptionType[] = TeamChoice;
  // let genderSelectOptions: SelectOptionType[] = GenderChoice;
  // let userTypeOptions: SelectOptionType[] = UserTypeChoice;

  // let teamSelected: SelectOptionType[] = [];
  // let genderSelected: SelectOptionType[] = [];
  // let userTypeSelected: SelectOptionType[] = [];
  // let locationSelected: SelectOptionType[] = [];
  // let reportingToSelected: SelectOptionType[] = [];

  const defaultDate = new Date(2000, 1, 1);
  const today = new Date();

  const year = defaultDate.getFullYear();
  const month = String(defaultDate.getMonth() + 1).padStart(2, "0"); // Adding 1 to month since months are zero-based
  const day = String(defaultDate.getDate()).padStart(2, "0");

  let formattedDefaultDate = `${year}-${month}-${day}`;
  let formattedJoiningDate = `${today.getFullYear()}-${today.getMonth()}-${today.getDate()}`;

  let errorMessage: string;
  let successMessage: string;

  let departmentOptions: SelectOptionsComponent = {
    optionsList: TeamChoice,
    selected: [TeamChoice[0]],
    isLabel: true,
    label: "Department",
    placeholder: "Select department",
    isTop: true
  };

  let genderOptions: SelectOptionsComponent = {
    optionsList: GenderChoice,
    selected: [GenderChoice[0]],
    isLabel: true,
    label: "Gender",
    placeholder: "Select gender",
    isTop: true
  };

  let userTypeOptions: SelectOptionsComponent = {
    optionsList: UserTypeChoice,
    selected: [],
    isLabel: true,
    label: "User type",
    placeholder: "Select user type",
    isTop: true
  };

  let locationOptions: SelectOptionsComponent = {
    optionsList: [],
    selected: [],
    isLabel: true,
    label: "Location",
    placeholder: "Select location",
    isTop: true
  };

  let usersOptions: SelectOptionsComponent = {
    optionsList: [],
    label: "Reporting to",
    selected: [],
    isTop: true,
    multiple: true
  };
</script>

<div class="bg-white p-3 card">
  <div class="card-body">
    <form>
      <div class="form-outline">
        <Input
          type="text"
          label={"First Name"}
          bind:value={registeration.first_name}
          handleInput={validateName}
          size={150}
          errorMessage="Invalid Name"
          hint={"please enter a valid first name"}
          placeholder={"Enter first name"}
          bind:isError={isErrorfName}
        />
      </div>
      <div class="form-outline">
        <Input
          type="text"
          label={"Last Name"}
          bind:value={registeration.last_name}
          handleInput={validateName}
          size={150}
          errorMessage="Invalid Name"
          hint={"please enter a valid last name"}
          placeholder={"Enter last name"}
          bind:isError={isErrorlName}
        />
      </div>
      <div class="form-outline">
        <Input
          type="text"
          label={"Email"}
          bind:value={registeration.email}
          handleInput={validateEmail}
          size={150}
          errorMessage="Invalid email address"
          hint={"please enter a valid email address"}
          placeholder={"Enter email address"}
          bind:isError={isErrormail}
        />
      </div>
      <div class="form-outline">
        <Input
          type="password"
          label={"Password"}
          bind:value={registeration.password}
          handleInput={validatePassword}
          size={150}
          errorMessage="Password is invalid"
          hint={"Password must be at least 8 characters and numbers."}
          placeholder={"please enter your password here"}
          bind:isError={isErrorpass}
        />
      </div>
      <div class="form-outline">
        <Input
          type="tel"
          label={"Mobile Number"}
          bind:value={registeration.mobile_number}
          handleInput={validatePhoneNumber}
          size={150}
          errorMessage="Invalid Mobile Number"
          hint={"please enter a valid mobile number in range(10, 15) digits"}
          placeholder={"01234567890"}
          bind:isError={isErrorMobile}
        />
      </div>
      <div class="form-outline">
        <Input
          type="text"
          label={"Role"}
          bind:value={registeration.job_title}
          handleInput={validateSpcialEmptyString}
          size={150}
          errorMessage="Role is invalid"
          hint={"please write a valid role"}
          placeholder={"please fill role here"}
          bind:isError={isErrorJobTitle}
        />
      </div>
      <div class="form-outline">
        <Input
          type="text"
          label={"Address"}
          bind:value={registeration.address}
          handleInput={validateSpcialEmptyString}
          size={150}
          errorMessage="Address is invalid"
          hint={"please write a valid address"}
          placeholder={"please put the address here"}
          bind:isError={isErrorAddress}
        />
      </div>
      <div class="form-outline">
        <Input
          type="text"
          label={"Social insurance number"}
          bind:value={registeration.social_insurance_number}
          handleInput={validateSpcialEmptyString}
          size={150}
          errorMessage="Social insurance number isinvalid"
          hint={"please write a valid Social insurance number"}
          placeholder={"please fill Social insurance number here"}
          bind:isError={isErrorSocialNumber}
        />
      </div>
      <div class="form-outline">
        <Input
          type="text"
          label={"Telegram User Name"}
          bind:value={registeration.telegram_link}
          handleInput={validateTelegramLink}
          size={150}
          errorMessage="Invalid Link"
          hint={"please enter a valid Telegram username link"}
          placeholder={"Enter telegram link e.g: @username"}
          bind:isError={isErrorLink}
        />
      </div>
      <div class="form-outline">
        <Input
          type="date"
          label={"Birthday date"}
          bind:value={formattedDefaultDate}
          handleInput={validateBirthday}
          size={150}
          errorMessage="Invalid birthdate"
          hint={"please enter a valid birthday date"}
          placeholder={"Enter birthday date"}
          bind:isError={isErrorBirthday}
        />
      </div>
      <div class="form-outline">
        <Input
          type="date"
          label={"Joining date"}
          bind:value={formattedJoiningDate}
          handleInput={validateBirthday}
          size={150}
          errorMessage="Invalid joining date"
          hint={"please enter a valid joining date"}
          placeholder={"Enter joining date"}
          bind:isError={isErrorJoiningDate}
        />
      </div>
      <div class="form-outline">
        <MultiSelect bind:options={departmentOptions} />
      </div>
      <div class="form-outline">
        <MultiSelect bind:options={genderOptions} />
      </div>
      <div class="form-outline">
        <MultiSelect bind:options={userTypeOptions} />
      </div>
      <div class="form-outline">
        <LocationSelect bind:options={locationOptions} />
      </div>
      <div class="form-outline">
        <PeopleSelect bind:options={usersOptions} />
      </div>
      <!-- RFNV1.0 <div class="form-outline">
                <Input
                    type="number"
                    label={'Net Current Salary'}
                    bind:value={registeration.salary.current_salary.net[0]}
                    handleInput={validateSalary}
                    size={20}
                    errorMessage="invalid salary value"
                    hint={'please enter the net current salary for the employee'}
                    placeholder={'Enter the net current salary'}
                    bind:isError={isErrorCurrentNetSalary}
                />
            </div> -->
      <!-- RFNV1.0 <div class="form-outline">
                <Input
                    type="number"
                    label={'Gross Current Salary'}
                    bind:value={registeration.salary.current_salary.gross[0]}
                    handleInput={validateSalary}
                    size={20}
                    errorMessage="invalid salary value"
                    hint={'please enter the gross current salary for the employee'}
                    placeholder={'Enter the gross current salary'}
                    bind:isError={isErrorCurrentGrossSalary}
                />
            </div> -->
      <!-- RFNV1.0 {#if salaryField[0]==true}
                <div class="form-outline">
                    <Input  
                        type="number"
                        label={'Net Joining Salary'}
                        bind:value={ registeration.salary.joining_salary.net[0]}
                        handleInput={validateSalary}
                        size={20}
                        errorMessage="invalid salary value"
                        hint={'please enter the net joining salary for the employee'}
                        placeholder={'Enter the net joining salary'}
                        bind:isError={isErrorNetJoinningSalary}
                    />
                </div>
            {/if} -->
      <!-- RFNV1.0 {#if salaryField[1] == true}
                <div class="form-outline">
                    <Input
                        type="number"
                        label={'Gross Joining Salary'}
                        bind:value={registeration.salary.joining_salary.gross[0]}
                        handleInput={validateSalary}
                        size={20}
                        errorMessage="invalid salary value"
                        hint={'please enter the gross joining salary for the employee'}
                        placeholder={'Enter the gross joining salary'}
                        bind:isError={isErrorGrossJoinningSalary}
                    />
                </div>
            {/if} -->
      <!-- RFNV1.0 {#if salaryField[2] == true}
                <div class="form-outline">
                    <Input
                        type="number"
                        label={'Net Salary before joining'}
                        bind:value={registeration.salary.net_salary_before_joining[0]}
                        handleInput={validateSalary}
                        size={20}
                        errorMessage="invalid salary value"
                        hint={'please enter the net salary before joining for the employee'}
                        placeholder={'Enter the net salary before joining'}
                        bind:isError={isErrorNetBeforeJoinningSalary}
                    />
                </div>
            {/if} -->
      <!-- RFNV1.0 {#if salaryField[3] == true}
                <div class="form-outline mb-3">
                    <Input
                        type="text"
                        label={'Benefits'}
                        bind:value={registeration.salary.benefits[0]}
                        handleInput={validateSalary}
                        size={20}
                        errorMessage="invalid salary value"
                        hint={'please enter the benefits for the employee'}
                        placeholder={'Enter the benefits'}
                        bind:isError={isErrorBenefits}
                    />
                </div>
            {/if} -->
      <!-- RFNV1.0 {#if showaddbutton}
                <div class="mb-4 d-flex justify-content-start mt-2">
                    <button type="button" class="btn btn-light minusbutton"
                        on:click|preventDefault={() => {
                            salaryField[thisSalaryInput] = true;
                            thisSalaryInput += 1
                            if (thisSalaryInput == 4){
                                showaddbutton = false;
                            } else {
                                showaddbutton = true;
                            }
                        }}
                    > Add More Salary
                    </button>
                </div>
            {/if} -->
      <div class="row">
        <div class="col-4">
          <!-- svelte-ignore a11y-label-has-associated-control -->
          <label>Profile Image</label>
        </div>
        <div class="col-8">
          <div class="form-outline">
            <SelectImage bind:image />
          </div>
        </div>
      </div>
      <div class="form-outline mt-4 d-flex justify-content-end">
        <Submit
          width={"15"}
          bind:successMessage
          bind:errorMessage
          label="Submit"
          onClick={async () => {
            isLoading = true;
            for (var i in usersOptions.selected) {
              registeration.reporting_to[i] = usersOptions.selected[i].value;
            }
            registeration.team = departmentOptions.selected[0].value;
            registeration.location = locationOptions.selected[0].value;
            registeration.gender = genderOptions.selected[0].value;
            registeration.user_type = userTypeOptions.selected[0].value;
            registeration.birthday = formattedDefaultDate;
            registeration.joining_at = formattedJoiningDate;
            if (image != undefined) {
              imageSrc = image.src;
              registeration.image = imageSrc;
            } else {
              registeration.image = "";
            }
            try {
              isError = false;
              await RegisterDataService.register(registeration);
              successMessage = "The user has been created successfully.";
              clearUserData(registeration);
            } catch (error) {
              errorMessage =
                "Fail to create a new user, please check what is missing in the data and try again.";
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
    </form>
  </div>
</div>

<svelte:head>
  <style>
    input {
      opacity: 1 !important;
    }
    .minusbutton {
      border: 1px solid rgb(18, 189, 26);
      height: 40px;
      max-height: 40px !important;
    }
    .minusbutton:hover {
      background-color: rgb(18, 189, 26) !important;
      color: #fff !important;
    }
  </style>
</svelte:head>
