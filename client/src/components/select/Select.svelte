<script>
  import MultiSelect from "svelte-multiselect";
  import LanguageSlot from "./LanguageSlot.svelte";

  export let options = [`Svelte`, `React`, `Vue`, `Angular`, `...`];

  let selected = [];
</script>

<code>selected = {JSON.stringify(selected)}</code>
<MultiSelect
  options={options}
  maxSelect={5}
  placeholder="What languages do you know?"
>
  <LanguageSlot let:option {option} slot="selected" />
  <LanguageSlot let:option {option} slot="option" />
<!--   <MinusIcon slot="remove-icon" width="1em" />
 --></MultiSelect>

<MultiSelect
  bind:selected
  {options}
  placeholder="Pick your favorite foods"
  removeAllTitle="Delete all foods"
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
/>
<!--   https://www.npmjs.com/package/svelte-multiselect -->
<!-- https://svelte-multiselect.netlify.app/#with-css-variables -->
