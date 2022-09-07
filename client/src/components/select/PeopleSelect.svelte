<script>
  import { onMount } from "svelte";
  onMount(async function () {
    const response = await fetch(
      "https://api.github.com/repos/sveltejs/svelte"
    );
    const data = await response.json();
    console.log(data);
  });
  import MultiSelect from "svelte-multiselect";
  import PeopleSlot from "./PeopleSlot.svelte";
  import LanguageSlot from "./PeopleSlot.svelte";

  export let options = [`Svelte`, `React`, `Vue`, `Angular`, `...`];
  export let selected = [];
  export let placeholder = `Select languages`;
  export let removeAllTitle = "Remove all";
</script>

<code>selected = {JSON.stringify(selected)}</code>
<MultiSelect
  {options}
  maxSelect={5}
  {placeholder}
  outerDivClass="foo"
  ulSelectedClass="bar"
  ulOptionsClass="baz"
  liOptionClass="bam"
  inputClass="slam"
  liSelectedClass="hi"
  liActiveOptionClass="mom"
  sortSelected={true}
  autocomplete="on"
  --sms-border-radius="5px"
  --sms-bg="#edf2f9"
  --sms-options-bg="white"
  --sms-min-height="20px"
  --sms-min-width="20px"
>
  <PeopleSlot let:option {option} slot="selected" />
  <PeopleSlot let:option {option} slot="option" />
</MultiSelect>

<MultiSelect bind:selected {options} {placeholder} {removeAllTitle} />
<!--   https://www.npmjs.com/package/svelte-multiselect -->
<!-- https://svelte-multiselect.netlify.app/#with-css-variables -->
