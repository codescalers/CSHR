<script lang="ts">
  import PeopleSelect from "../ui/select/UsersMultiSelect.svelte";
  import type { SelectOptionType } from "../../utils/types";
  import Submit from "../ui/Button.svelte";
  import Input from "../ui/Input.svelte";
  import UserDataService from "../../apis/users/users";
  import SelectImage from "../ui/select/SelectImage.svelte";

  export let isLoading: boolean = false;
  export let isError: boolean = false;

  let documentNameValue: string;
  let image: HTMLImageElement;
  let documentNameIsError: boolean | null = null;

  $: submitDisabled =
    documentNameIsError === null || documentNameIsError === true;

  let eventPeopleIsError: boolean | null = null;
  let peopleSelected: SelectOptionType[] = [];

  let successMessage: string;
  let errorMessage: string;
</script>

<div class="bg-white p-3 card">
  <div class="card-body">
    <form enctype="multipart/form-data">
      <div class="row d-flex justify-content-center align-items-center">
        <div class="col-12">
          <PeopleSelect
            bind:isError={eventPeopleIsError}
            bind:selected={peopleSelected}
            mylabel={"Select User"}
            multiple={false}
            isTop={false}
          />
        </div>
        <div class="col-12">
          <Input
            type="text"
            label={"Document Name"}
            bind:value={documentNameValue}
            handleInput={() => {
              return false;
            }}
            size={20}
            errorMessage="Document name is invalid"
            hint={"please write a valid document name"}
            bind:isError={documentNameIsError}
            placeholder="Enter Document Name"
          />
        </div>
        <div class="col-12">
          <SelectImage bind:image />
        </div>
        <div class="col-12 mt-4 d-flex justify-content-end">
          <Submit
            width={"15"}
            bind:successMessage
            bind:errorMessage
            label="Submit"
            onClick={async () => {
              isLoading = true;
              try {
                await UserDataService.postUserDocument({
                  user: peopleSelected[0].value,
                  name: documentNameValue,
                  image: image.src,
                });
                successMessage = "The document has been added.";
              } catch (error) {
                errorMessage =
                  "Error while trying to add the document, please check the provided data and try again.";
                isError = true;
              } finally {
                isLoading = false;
                documentNameValue = "";
                peopleSelected = [];
                image.src = "";
              }
              return isError;
            }}
            className=""
            bind:disabled={submitDisabled}
          />
        </div>
      </div>
    </form>
  </div>
</div>
