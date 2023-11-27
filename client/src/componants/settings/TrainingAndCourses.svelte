<script lang="ts">
  import TrainingAndCourses from "../../apis/training_and_courses/trainingAndCourses";
  import { UserStore } from "../../utils/stores";
  import { validateLink } from "../../utils/validations";
  import Submit from "../ui/Button.svelte";
  import Input from "../ui/Input.svelte";

  export let isLoading = false;
  export let isError = false;

  let isErrorName: null | boolean,
    isErrorLink: null | boolean = null;
  let CourseName: string, certificateLink: string;

  $: submitDisabled =
    isErrorName == true ||
    isErrorName == null ||
    isErrorLink == true ||
    isErrorLink == null;

  let errorMessage: string;
  let successMessage: string;
</script>

<h5>
  This section related to <span class="text-primary">Training and courses</span>
</h5>
<div class="row">
  <div class="col-12">
    <div class="form-outline">
      <Input
        type="text"
        label={"Course Name"}
        bind:value={CourseName}
        handleInput={() => {
          return false;
        }}
        size={150}
        errorMessage="Invalid Course Name"
        hint={"please enter a valid course name"}
        placeholder={"Enter course name"}
        bind:isError={isErrorName}
      />
    </div>
  </div>
  <div class="col-12">
    <div class="form-outline">
      <Input
        type="text"
        label={"Certificate Link"}
        bind:value={certificateLink}
        handleInput={validateLink}
        size={150}
        errorMessage="Invalid Course Link"
        hint={"please enter a valid course link"}
        placeholder={"Enter course link"}
        bind:isError={isErrorLink}
      />
    </div>
  </div>
  <div class="col-12">
    <div class="form-outline mt-4 d-flex justify-content-end">
      <Submit
        width={"30"}
        bind:successMessage
        bind:errorMessage
        label="Submit"
        onClick={async () => {
          isLoading = true;
          try {
            await TrainingAndCourses.post({
              name: CourseName,
              certificate_link: certificateLink,
              user_id: $UserStore.id
            });
            successMessage = "A new course has been added successfully.";
          } catch (error) {
            errorMessage =
              "an error happened while adding a new course, please check the data and try again.";
            isError = true;
          } finally {
            CourseName = "";
            certificateLink = "";
            isLoading = false;
          }
          return isError;
        }}
        className=""
        bind:disabled={submitDisabled}
      />
    </div>
  </div>
</div>
