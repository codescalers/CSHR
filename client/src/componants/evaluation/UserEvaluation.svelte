<script lang="ts">
  import evaluationDataService from "../../apis/evaluation/Evaluation";
  import type { SelectOptionType } from "../../utils/types";
  import { validateLink } from "../../utils/validations";
  import Submit from "../ui/Button.svelte";
  import Input from "../ui/Input.svelte";
  import MultiSelect from "../ui/select/MultiSelect.svelte";
  import PeopleSelect from "../ui/select/UsersMultiSelect.svelte";

  export let isLoading = false;
  export let isError = false;

  let evaluation_quartur_options: SelectOptionType[] = [
    { label: "1 : 3", value: "1 : 3" },
    { value: "4 : 6", label: "4 : 6" },
    { value: "7 : 9", label: "7 : 9" },
    { value: "10 : 12", label: "10 : 12" },
  ];

  let evaluation_quartur_selected: SelectOptionType[] = [];
  let evaluationLinkValue: string;
  let evaluationScoreValue: number;
  let evaluationLinkIsError: boolean | null = null;
  let evaluationScoreError: boolean | null = null;

  $: submitDisabled =
    evaluationLinkIsError === null ||
    evaluationScoreError === null ||
    evaluationLinkIsError === true ||
    evaluationScoreError === true ||
    evaluation_quartur_selected.length === 0;

  let eventPeopleIsError: boolean | null = null;
  let peopleSelected: SelectOptionType[] = [];

  let successMessage: string;
  let errorMessage: string;
</script>

<div class="bg-white p-3 card">
  <div class="card-body">
    <form>
      <div class="row d-flex justify-content-center align-items-center">
        <div class="col-12">
          <PeopleSelect
            bind:isError={eventPeopleIsError}
            bind:selected={peopleSelected}
            mylabel={"Select User"}
            multiple={false}
            isTop={true}
          />
        </div>
        <div class="col-12">
          <MultiSelect
            bind:options={evaluation_quartur_options}
            bind:selected={evaluation_quartur_selected}
            isLabel={true}
            label="Evaluation Quartur"
            placeholder="Select Evaluation Quartur"
            removeAllTitle="Remove all Evaluation Quartur"
            multiple={false}
          />
        </div>
        <div class="col-12">
          <Input
            type="url"
            label={"Evaluation Link"}
            bind:value={evaluationLinkValue}
            handleInput={validateLink}
            size={20}
            errorMessage="Evaluation Link is invalid"
            hint={"please write a valid link"}
            bind:isError={evaluationLinkIsError}
            placeholder="Enter Evaluation Link"
          />
        </div>
        <div class="col-12">
          <Input
            type="number"
            label={"Score"}
            bind:value={evaluationScoreValue}
            handleInput={() => {
              return false;
            }}
            size={20}
            errorMessage="Score must be a number"
            hint={"Please write a valid number"}
            bind:isError={evaluationScoreError}
            placeholder="Enter score value"
          />
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
                await evaluationDataService.postUserEvaluation({
                  user: peopleSelected[0].value,
                  quarter: evaluation_quartur_selected[0].value,
                  link: evaluationLinkValue,
                  score: evaluationScoreValue,
                });

                successMessage = "The new user evaluation is submitted successfully.";
              } catch (error) {
                errorMessage = "The new user evaluation submission failed.";
                isError = true;
              } finally {
                isLoading = false;
                evaluationLinkValue = "";
                peopleSelected = [];
                evaluation_quartur_selected = [];
                evaluationScoreValue = 0;
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
