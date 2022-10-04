<script lang="ts">
  import type { SelectOptionType } from '../select/types';
  import MultiSelect from '../select/MultiSelect.svelte';
  import Submit from '../submit/Submit.svelte';
  import Input from '../input/Input.svelte';
  import evaluationDataService from '../../services/axios/evaluation/EvaluationDataService';
  export let isLoading: boolean = false;
  export let isError: boolean = false;
  let evaluation_form_options: SelectOptionType[] = [
    { label: 'Peer 2 Peer Form', value: 'Peer 2 Peer Form' },
    { label: 'Reverse Form', value: 'Reverse Form' },
  ];

  let evaluation_quartur_options: SelectOptionType[] = [
    { label: '1 : 3', value: '1 : 3' },
    { value: '4 : 6', label: '4 : 6' },
    { value: '7 : 9', label: '7 : 9' },
    { value: '10 : 12', label: '10 : 12' },
  ];
  let evaluation_form_selected: SelectOptionType[] = [];
  let evaluation_quartur_selected: SelectOptionType[] = [];
  let evaluationLinkValue: string;
  let evaluationLinkIsError: boolean | null = null;
  $: submitDisabled =
    evaluationLinkIsError === null ||
    evaluationLinkIsError === true ||
    evaluation_form_selected.length === 0 ||
    evaluation_quartur_selected.length === 0;
</script>

<form>
  <MultiSelect
    bind:options={evaluation_form_options}
    bind:selected={evaluation_form_selected}
    isLabel={true}
    placeholder="Select Evaluation Form"
    removeAllTitle="Remove all Evaluation Form"
    label="Evaluation Form"
    multiple={false}
  />

  <MultiSelect
    bind:options={evaluation_quartur_options}
    bind:selected={evaluation_quartur_selected}
    isLabel={true}
    label="Evaluation Quartur"
    placeholder="Select Evaluation Quartur"
    removeAllTitle="Remove all Evaluation Quartur"
    multiple={false}
  />

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
  <div class="mt-5 col-3">
    <Submit
      successMessage={'Evaluation is Submitted'}
      errorMessage={' Evaluation Submission Failed'}
      label="Submit"
      onClick={async () => {
        isLoading = true;
        try {
          /*    await CalendarDataService.postMeeting({
          hostedUserID: $UserStore.id,
          date: startDate,
          invitedUsers: invited_people,
          location: meetingLocationValue,
          meetingLink: meetingLinkValue,
          time: meetingTimeValue,
        
        }); */

          await evaluationDataService.postEvaluation({
            form: evaluation_form_selected[0].value,
            quarter: evaluation_quartur_selected[0].value,
            link: evaluationLinkValue,
          });
        } catch (error) {
          isError = true;
        } finally {
          isLoading = false;
          evaluationLinkValue = '';
          evaluation_form_selected = [];
          evaluation_quartur_selected = [];
        }
        return isError;
      }}
      className=""
      bind:disabled={submitDisabled}
    />
  </div>
</form>

<form />
