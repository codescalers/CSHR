<script lang="ts">
  import Tags from 'svelte-tags-input'
  import { onMount } from 'svelte';
  import SkillsDataService from "../../services/axios/skills/skills"
  import Submit from '../submit/Submit.svelte';
  import {UserStore} from "../../stores"
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

<h5>This section realted to <span class="text-primary">User Skills</span></h5>

<div class="form-outline">
  <div class="row">
    <div class="col-4">
      <!-- svelte-ignore a11y-label-has-associated-control -->
      <label class="col-form-label py-3">Add new skills</label>
    </div>
    <div class="col-8">
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
  <div class="form-outline mt-4 d-flex justify-content-end">
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