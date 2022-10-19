<script lang="ts">
    import PeopleSelect from '../select/PeopleSelect.svelte';
    import type { SelectOptionType } from '../../types';
    import Submit from '../submit/Submit.svelte';
    import Input from '../input/Input.svelte';
    import UserDataService from '../../services/axios/user/UserDataService';
    import SelectImage from '../select/SelectImage.svelte';

    export let isLoading: boolean = false;
    export let isError: boolean = false;

    let documentNameValue: string;
    let image: HTMLImageElement;
    let documentNameIsError: boolean | null = null;

    $: submitDisabled =
        documentNameIsError === null ||
        documentNameIsError === true;

    let eventPeopleIsError: boolean | null = null;
    let peopleSelected: SelectOptionType[] = [];
</script>


<form enctype="multipart/form-data">
    <div class="row d-flex justify-content-center align-items-center">
        <div class="col-12">
            <PeopleSelect
                bind:isError={eventPeopleIsError}
                bind:selected={peopleSelected}
                mylabel= {"Select User"}
                multiple={false}
            />
        </div>
          <div class="col-12">
            <Input
                type="text"
                label={'Document Name'}
                bind:value={documentNameValue}
                handleInput={() => {
                    return false;
                }}
                size={20}
                errorMessage="Document name is invalid"
                hint={'please write a valid document name'}
                bind:isError={documentNameIsError}
                placeholder="Enter Document Name"
            />
        </div>
          <div class="col-12">
            <SelectImage bind:image />
          </div>
        <div class="col-12 mt-4  d-flex justify-content-end">
            <Submit
              width={'15'}
              successMessage={'Evaluation is Submitted'}
              errorMessage={' Evaluation Submission Failed'}
              label="Submit"
              onClick={async () => {
                isLoading = true;
                try {
                  await UserDataService.postUserDocument({
                    user: peopleSelected[0].value,
                    name: documentNameValue,
                    image: image.src
                  });
                } catch (error) {
                  isError = true;
                } finally {
                  isLoading = false;
                  documentNameValue = '';
                  peopleSelected = [];
                  image.src = "" 
                }
                return isError;
              }}
              className=""
              bind:disabled={submitDisabled}
            />
        </div>
    </div>
</form>