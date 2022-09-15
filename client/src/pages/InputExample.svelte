<script lang="ts">
  import Input from "../components/input/Input.svelte";
  import Select from "../components/select/PeopleSelect.svelte";

  import Sidebar from "../components/sidebar/Sidebar.svelte";
  const handleInput = (e: any): boolean => {
    if (e.target.value !== "omar") return true;
    return false;
  };
  let inputValue = "";
  let isError: null | boolean = null;
</script>

<Sidebar>
  <span slot="page-name">Calendar</span>
  <section class="fluid-container mt-5 content" slot="content">
    <Input
      type="text"
      label={"name"}
      bind:value={inputValue}
      {handleInput}
      size={255}
      errorMessage="Name is invalid"
      hint={"please write omar"}
      placeholder={"please enter your name here"}
      bind:isError
    />

    <Select />
  </section>
</Sidebar>

<style>
  .content {
    height: fit-content;
  }
</style>
