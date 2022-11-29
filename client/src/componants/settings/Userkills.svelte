<script lang="ts">
  import Tags from 'svelte-tags-input'
  import { onMount } from 'svelte';
  import SkillsDataService from "../../apis/skills/skills"
  import Submit from '../ui/Button.svelte';
  import { UserStore } from "../../utils/stores"

  export let isLoading: boolean = false;
  export let isError: boolean = false;

  let skills: string[] = [];
  let tag: string = "";

  onMount(async function () {
    const skillsApi = await SkillsDataService.getAll();
    for (let skill in skillsApi) {
      skills.push(skillsApi[skill].name);
    };
  });
  
  function handleTags(event: { detail: { tags: string; }; }) {
      tag = event.detail.tags;
  }

  $: submitDisabled = 
    tag == "" || tag == null || tag == undefined;

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
          width={'30'}
          successMessage={'Skills Added!'}
          errorMessage={'Skills added failed!'}
          label="Submit"
          onClick={async () => {
            isLoading = true;
            let tags = String(tag).split(',')
              try {
                await SkillsDataService.postSkills($UserStore, tags);
              } catch (error) {
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
  .absolute{
    position: absolute;
    bottom: -10px;
    left: 0px;
    width: 100%;
  }
</style>