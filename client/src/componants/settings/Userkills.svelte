<script lang="ts">
  import { onMount } from "svelte";
  import Tags from "svelte-tags-input";

  import SkillsDataService from "../../apis/skills/skills";
  import { UserStore } from "../../utils/stores";
  import Submit from "../ui/Button.svelte";

  export let isLoading = false;
  export let isError = false;

  let skills: string[] = [];
  let tag = "";

  onMount(async function () {
    const skillsApi = await SkillsDataService.getAll();
    for (let skill in skillsApi) {
      skills.push(skillsApi[skill].name);
    }
  });

  function handleTags(event: { detail: { tags: string } }) {
    tag = event.detail.tags;
  }

  $: submitDisabled = tag == "" || tag == null || tag == undefined;

  let successMessage: string;
  let errorMessage: string;
</script>

<h5>This section related to <span class="text-primary">User Skills</span></h5>

<div class="form-outline">
  <div class="row pt-1">
    <div class="col-4">
      <!-- svelte-ignore a11y-label-has-associated-control -->
      <label class="col-form-label py-3">Add new skills</label>
    </div>
    <div class="col-8 pt-2">
      <Tags
        on:tags={handleTags}
        maxTags={8}
        allowPaste={true}
        allowDrop={true}
        splitWith={"/"}
        onlyUnique={true}
        placeholder={"Select skill or choices on from suggestions"}
        autoComplete={skills}
        name={"custom-name"}
        id={"custom-id"}
        allowBlur={true}
        disable={false}
        minChars={1}
      />
    </div>
  </div>
</div>
<div class="col-12">
  <div class="absolute form-outline">
    <Submit
      width={"30"}
      bind:successMessage
      bind:errorMessage
      label="Submit"
      onClick={async () => {
        isLoading = true;
        let tags = String(tag).split(",");
        try {
          await SkillsDataService.postSkills($UserStore, tags);
          successMessage = "The new skills have been added successfully.";
        } catch (error) {
          errorMessage =
            "Error while trying to add the new skills, please check the provided data and try again.";
          isError = true;
        } finally {
          isLoading = false;
          tag = "";
        }
        return isError;
      }}
      className=""
      bind:disabled={submitDisabled}
    />
  </div>
</div>

<style>
  .absolute {
    position: absolute;
    bottom: -10px;
    left: 0px;
    width: 100%;
  }
</style>
