<script lang="ts">
    import PeopleSelect from '../select/PeopleSelect.svelte';
    import type { SelectOptionType } from '../../types';
    import MultiSelect from '../select/MultiSelect.svelte';
    import Submit from '../submit/Submit.svelte';
    import Input from '../input/Input.svelte';
    import evaluationDataService from '../../services/axios/evaluation/EvaluationDataService'

    export let isLoading: boolean = false;
    export let isError: boolean = false;

    let evaluation_quartur_options: SelectOptionType[] = [
        { label: '1 : 3', value: '1 : 3' },
        { value: '4 : 6', label: '4 : 6' },
        { value: '7 : 9', label: '7 : 9' },
        { value: '10 : 12', label: '10 : 12' },
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
</script>


<form>
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
                label={'Evaluation Link'}
                bind:value={evaluationLinkValue}
                handleInput={() => {
                    return false;
                }}
                size={20}
                errorMessage="Evaluation Link is invalid"
                hint={'please write a valid link'}
                bind:isError={evaluationLinkIsError}
                placeholder="Enter Evaluation Link"
            />
        </div>
          <div class="col-12">
            <Input
                type="number"
                label={'Score'}
                bind:value={evaluationScoreValue}
                handleInput={() => {
                    return false;
                }}
                size={20}
                errorMessage="Score must be a number"
                hint={'Please write a valid number'}
                bind:isError={evaluationScoreError}
                placeholder="Enter score value"
            />
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
                  await evaluationDataService.postUserEvaluation({
                    user: peopleSelected[0].value,
                    quarter: evaluation_quartur_selected[0].value,
                    link: evaluationLinkValue,
                    score: evaluationScoreValue
                  });
                } catch (error) {
                  isError = true;
                } finally {
                  isLoading = false;
                  evaluationLinkValue = '';
                  peopleSelected = []
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