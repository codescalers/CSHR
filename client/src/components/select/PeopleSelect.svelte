<script lang="ts">
  import userDataService from "../../services/axios/users/UserDataService";
  import { onMount } from "svelte";
  import PeopleSlot from "./PeopleSlot.svelte";
  import MultiSelect from "svelte-multiselect";
  export let selected: any[] = [];
  export let maxSelect: number | null = null;
  export let placeholder = `Select Users`;
  export let removeAllTitle = "Remove all users";
  let options: any[] = [];
  onMount(async () => {
    let { data } = await userDataService.getAll();
    options = data.map((user: any) => {
      return {
        id: user.id,
        full_name: user.full_name,
        image: user.image,
      };
    });
  });
</script>

<code>selected = {JSON.stringify(selected)}</code>
<MultiSelect
  {options}
  {maxSelect}
  {placeholder}
  bind:selected
  outerDivClass="foo"
  ulSelectedClass="bar"
  ulOptionsClass="baz"
  liOptionClass="bam"
  inputClass="slam"
  liSelectedClass="hi"
  liActiveOptionClass="mom"
  sortSelected={true}
  autocomplete="on"
  --sms-border-radius="0.3rem"
  --sms-bg="#edf2f9"
  --sms-options-bg="white"
  --sms-min-height="3rem"
  --sms-min-width="4rem"
>
  <PeopleSlot let:option {option} slot="selected" />
  <PeopleSlot let:option {option} slot="option" />
</MultiSelect>

<!--   https://www.npmjs.com/package/svelte-multiselect -->
<!-- https://svelte-multiselect.netlify.app/#with-css-variables -->
