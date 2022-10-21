<script lang="ts">
    import { validateLink } from '../../services/utils/validators';
    import TrainingAndCourses  from "../../services/axios/training_and_courses/trainingAndCourses"
    import Input from '../input/Input.svelte';
    import Submit from '../submit/Submit.svelte';
    import { UserStore } from "../../stores"
    export let isLoading: boolean = false;
    export let isError: boolean = false;
    
    let isErrorName: null | boolean,
        isErrorLink: null | boolean = null
    let CourseName: string, certificateLink: string;
    
    $: submitDisabled = 
        isErrorName == true || isErrorName == null ||
        isErrorLink == true || isErrorLink == null
</script>

<h5>This section realted to <span class="text-primary">Training and courses</span></h5>
<div class="row">
    <div class="col-12">
        <div class="form-outline">
            <Input
                type="text"
                label={'Course Name'}
                bind:value={ CourseName }
                handleInput={ () => {return false;}}
                size={150}
                errorMessage="Invalid Course Name"
                hint={'please enter a valid course name'}
                placeholder={'Enter course name'}
                bind:isError={ isErrorName }
            /> 
        </div>
    </div>
    <div class="col-12">
        <div class="form-outline">
            <Input
                type="text"
                label={'Certificate Link'}
                bind:value={ certificateLink }
                handleInput={validateLink}
                size={150}
                errorMessage="Invalid Course Link"
                hint={'please enter a valid course link'}
                placeholder={'Enter course link'}
                bind:isError={ isErrorLink }
            /> 
        </div>
    </div>
    <div class="col-12">
        <div class="form-outline mt-4 d-flex justify-content-end">
            <Submit
                width={'30'}
                successMessage={'Training and Courses Updated!'}
                errorMessage={'Training and Courses failed!'}
                label="Submit"
                onClick={async () => {
                    isLoading = true;
                    try {
                        await TrainingAndCourses.post(
                            {name: CourseName, certificate_link: certificateLink, user_id: $UserStore.id}
                        );
                    } catch (error) {
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