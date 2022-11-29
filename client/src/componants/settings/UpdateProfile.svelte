<script lang="ts">
    import Input from '../ui/Input.svelte';
    import Submit from '../ui/Button.svelte';
    import MultiSelect from '../ui/select/MultiSelect.svelte';
    import { UserStore } from '../../utils/stores';
    import type { SelectOptionType } from '../../utils/types';
    import { 
        validateBirthday,
        validateEmail,
        validateName,
        validatePhoneNumber,
        validateSalary,
        validateTelegramLink,
    } from '../../utils/validations';
    import { TeamChoice, GenderChoice, UserTypeChoice } from '../../utils/choices';
    import LocationSelect from '../ui/select/LocationSelect.svelte';
    import PeopleSelect from '../ui/select/UsersMultiSelect.svelte';
    import SelectImage from '../ui/select/SelectImage.svelte';
    import ColorPicker from './ColorPicker.svelte';
    import { Color } from 'color-picker-svelte'
    import RegisterDataService from '../../apis/users/users';
    import RemoveImage from './RemoveImage.svelte';
    export let user: any;
    export let isLoading: boolean = false;
    export let isError: boolean = false;

    let defaultNetSalary: number;
    let defaultGrossSalary: number;
    let image: HTMLImageElement;
    let color = new Color(user.background_color)
    let removeImage: boolean = false;

    if (user.salary.current_salary){
        defaultNetSalary = +user.salary.current_salary.net[0];
    } else {
        defaultNetSalary = 0
    }

    if (user.salary.current_salary){
        defaultGrossSalary = +user.salary.current_salary.gross[0];
    } else {
        defaultGrossSalary = 0
    }

    let isErrorfName: null | boolean,
        isErrorlName: null | boolean,
        isErrormail: null | boolean,
        isErrorMobile: null | boolean,
        isErrorJobTitle: null | boolean,
        isErrorAddress: null | boolean,
        isErrorLink: null | boolean,
        isErrorSocialNumber: null | boolean,
        isErrorUserType: null | boolean,
        isErrorLocation: null | boolean,
        isErrorSuperuser: null | boolean,
        isErrorCurrentNetSalary: null | boolean,
        isErrorCurrentGrossSalary: null | boolean,
        isErrorBirthday: null | boolean
    = null;

    $: submitDisabled = 
        isErrorCurrentGrossSalary == true || isErrorCurrentNetSalary == true ||
        isErrorBirthday == true || isErrorLink == true ||
        isErrorJobTitle == true || isErrorMobile == true ||
        isErrorSocialNumber == true || isErrorlName == true || isErrorfName == true ||
        isErrorAddress == true 

    let teamSelectOptions: SelectOptionType[] = TeamChoice;
    let genderSelectOptions: SelectOptionType[] = GenderChoice;
    let userTypeOptions: SelectOptionType[] = UserTypeChoice;

    let teamSelected: SelectOptionType[] = [{"label": user.team, "value": user.team}];
    let genderSelected: SelectOptionType[] = [{"label": user.gender, "value": user.gender}];
    let userTypeSelected: SelectOptionType[] = [{"label": user.user_type, "value": user.user_type}];
    let locationSelected: SelectOptionType[] = [{"label": user.location.name, "value": user.location.name}];
    let reportingToSelected: SelectOptionType[] = [];

    for (let i in user.reporting_to) {
        reportingToSelected.push({"label": user.reporting_to[i].full_name, "value": user.reporting_to[i].id});
    }

</script>

<div class="card">
    <div class="card-body">
        <div class="row">
            <div class="col-6">
                <div class="form-outline">
                    <Input
                        type="text"
                        label={'First Name'}
                        bind:value={ user.first_name }
                        handleInput={validateName}
                        size={150}
                        errorMessage="Invalid Name"
                        hint={'please enter a valid first name'}
                        placeholder={'Enter first name'}
                        bind:isError={isErrorfName}
                    /> 
                </div>
            </div>
            <div class="col-6">
                <div class="form-outline">
                    <Input
                        type="text"
                        label={'Last Name'}
                        bind:value={ user.last_name }
                        handleInput={validateName}
                        size={150}
                        errorMessage="Invalid Name"
                        hint={'please enter a valid last name'}
                        placeholder={'Enter last name'}
                        bind:isError={isErrorlName}
                    /> 
                </div>
            </div>
            {#if $UserStore.user_type == "Admin"}
                <div class="col-6">
                    <div class="form-outline">
                        <Input
                            type="text"
                            label={'Email'}
                            bind:value={ user.email }
                            handleInput={validateEmail}
                            size={150}
                            errorMessage="Invalid email address"
                            hint={'please enter a valid email address'}
                            placeholder={'Enter email address'}
                            bind:isError={isErrormail}
                        /> 
                    </div>
                </div>
                <div class="col-6">
                    <div class="form-outline">
                        <Input
                            type="text"
                            label={'Social insurance number'}
                            bind:value={user.social_insurance_number}
                            handleInput={() => {
                                return false;
                            }}
                            size={150}
                            errorMessage="Social insurance number isinvalid"
                            hint={'please write a valid Social insurance number'}
                            placeholder={'please fill Social insurance number here'}
                            bind:isError={isErrorSocialNumber}
                        />
                    </div>
                </div>
                <div class="col-6">
                    <div class="form-outline">
                        <Input
                            type="number"
                            label={'Net Current Salary'}
                            bind:value={ defaultNetSalary }
                            handleInput={validateSalary}
                            size={20}
                            errorMessage="invalid salary value"
                            hint={'please enter the net current salary for the employee'}
                            placeholder={'Enter the net current salary'}
                            bind:isError={isErrorCurrentNetSalary}
                        />
                    </div>
                </div>
                <div class="col-6">
                    <div class="form-outline">
                        <Input
                            type="number"
                            label={'Gross Current Salary'}
                            bind:value={ defaultGrossSalary }
                            handleInput={validateSalary}
                            size={20}
                            errorMessage="invalid salary value"
                            hint={'please enter the gross current salary for the employee'}
                            placeholder={'Enter the gross current salary'}
                            bind:isError={isErrorCurrentGrossSalary}
                        />
                    </div>
                </div>
                <div class="col-6">
                    <div class="form-outline">
                        <MultiSelect
                          bind:options={teamSelectOptions}
                          bind:selected={teamSelected}
                          isLabel={true}
                          label="Team"
                          placeholder="Select team"
                          removeAllTitle="Remove all teams"
                          multiple={false}
                        />
                    </div>
                </div>
                <div class="col-6">
                    <div class="form-outline">
                        <MultiSelect
                          bind:options={genderSelectOptions}
                          bind:selected={genderSelected}
                          isLabel={true}
                          label="Gender"
                          placeholder="Select gender"
                          removeAllTitle="Remove gender"
                          multiple={false}
                        />
                    </div>
                </div>
                <div class="col-6">
                    <div class="form-outline">
                        <MultiSelect
                          bind:options={userTypeOptions}
                          bind:selected={userTypeSelected}
                          isLabel={true}
                          label="User Type"
                          placeholder="Select user type"
                          removeAllTitle="Remove user type"
                          multiple={false}
                          bind:isError={isErrorUserType}
                        />
                    </div>
                </div>
                <div class="col-6">
                    <div class="form-outline">
                        <LocationSelect
                            mylabel= {"Location"}
                            bind:isError={isErrorLocation}
                            bind:selected={locationSelected}
                            isTop={true}
                        />
                    </div>
                </div>
                <div class="col-6">
                    <div class="form-outline">
                        <PeopleSelect
                            multiple={true}
                            mylabel= {"Reporting to"}
                            bind:isError={isErrorSuperuser}
                            bind:selected={reportingToSelected}
                            isTop={true}
                        />
                    </div>
                </div>
            {/if}
            <div class="col-6">
                <div class="form-outline">
                    <Input
                        type="tel"
                        label={'Mobile Number'}
                        bind:value={ user.mobile_number }
                        handleInput={validatePhoneNumber}
                        size={150}
                        errorMessage="Invalid Mobile Number"
                        hint={'please enter a valid mobile number in range(10, 15) digits'}
                        placeholder={'01234567890'}
                        bind:isError={isErrorMobile}
                    />
                </div>
            </div>
            <div class="col-6">
                <div class="form-outline">
                    <Input
                        type="text"
                        label={'Job Title'}
                        bind:value={ user.job_title }
                        handleInput={() => {
                            return false;
                        }}
                        size={150}
                        errorMessage="job title is invalid"
                        hint={'please write a valid job title'}
                        placeholder={'please fill job title here'}
                        bind:isError={isErrorJobTitle}
                    />
                </div>
            </div>
            <div class="col-6">
                <div class="form-outline">
                    <Input
                        type="text"
                        label={'Address'}
                        bind:value={ user.address }
                        handleInput={() => {
                            return false;
                        }}
                        size={150}
                        errorMessage="Address is invalid"
                        hint={'please write a valid address'}
                        placeholder={'please put the address here'}
                        bind:isError={isErrorAddress}
                    />
                </div>
            </div>
            <div class="col-6">
                <div class="form-outline">
                    <Input
                        type="text"
                        label={'Telegram User Name'}
                        bind:value={ user.telegram_link }
                        handleInput={validateTelegramLink}
                        size={150}
                        errorMessage="Invalid Link"
                        hint={'please enter a valid Telegram username link'}
                        placeholder={'Enter telegram link e.g: @username'}
                        bind:isError={isErrorLink}
                    />
                </div>
            </div>
            <div class="col-6">
                <div class="form-outline">
                    <Input
                        type="date"
                        label={'Birthday date'}
                        bind:value={ user.birthday }
                        handleInput={validateBirthday}
                        size={150}
                        errorMessage="Invalid birthdate"
                        hint={'please enter a valid birthday date'}
                        placeholder={'Enter birthday date'}
                        bind:isError={isErrorBirthday}
                    />
                </div>
            </div>
            <div class="col-6 mt-3">
                <div class="form-outline">
                    <div class="row">
                        <div class="col-4 d-flex align-items-center">Background Logo color</div>
                        <div class="col-8">
                            <ColorPicker bind:color/>
                        </div>
                    </div>
                </div>
            </div>
            {#if user.image.includes("profile_image") }
                <div class="col-6 mt-3">
                    <RemoveImage on:message={(event) => {
                        removeImage = event.detail.text
                    }} buttonBackgraound={user.background_color} label={"Clear Profile Image"}/>
                </div>
            {/if}
            <div class="col-6">
                <div class="row">
                    <div class="col-6 mt-3">
                        <!-- svelte-ignore a11y-label-has-associated-control -->
                        <label>Profile Image</label>
                    </div>
                    <div class="col-6">
                        <div class="form-outline mt-3">
                            <SelectImage bind:image styleOnRow={"flex-direction: column;"}/>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-12">
                <div class="form-outline mt-4  d-flex justify-content-center">
                    <Submit
                        width={'15'}
                        successMessage={'Profile Updated!'}
                        errorMessage={'Profile updates failed!'}
                        label="Submit"
                        onClick={async () => {
                            isLoading = true;
                            for (var i in reportingToSelected) {
                                user.reporting_to[i]=reportingToSelected[i].value;
                            }
                            user.background_color = color.toHexString()
                            user.team = teamSelected[0].value;
                            user.location = locationSelected[0].value;
                            user.gender = genderSelected[0].value;
                            user.user_type = userTypeSelected[0].value;
                            user.remove_image = removeImage
                            if (image != undefined){
                                user.image = image.src
                            } else {
                                user.image = ""
                            }
                            try {
                                await RegisterDataService.updateProfile(user);
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
            </div>
        </div>
    </div>
</div>