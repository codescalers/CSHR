<script lang="ts">
  import { onMount } from "svelte";
  import { useParams } from "svelte-navigator";

  import usersAPI from "../../apis/users/users";
  import NotFound from "../../pages/Error.svelte";
  import { UserStore } from "../../utils/stores";
  import type {
    AdminViewInterface,
    SupervisorViewInterface,
    UserInterface
  } from "../../utils/types";
  // import Certificates from "./Certificates.svelte";
  import Company from "./Company.svelte";
  // import Evaluation from "./Evaluation.svelte";
  import ProfileImage from "./ProfileImage.svelte";
  import ReportTo from "./ReportTo.svelte";
  // import Salary from "./Salary.svelte";
  import UserData from "./UserData.svelte";
  // import UserDocuments from "./UserDocuments.svelte";
  // import Skills from "./UserSkills.svelte";
  import VacationBalance from "./VacationBalance.svelte";

  const params = useParams();
  let id = Number($params.id);

  export let isLoading = false;
  export let isError: boolean | null = null;

  let user:
    | AdminViewInterface
    | SupervisorViewInterface
    | UserInterface
    | null = null;

  onMount(async () => {
    document.getElementById("body-pd")!.style.overflow = "auto";
    isLoading = true;
    try {
      if ($UserStore !== undefined && $UserStore.id === id) {
        user = $UserStore;
      } else {
        user = await usersAPI.getByIdBasedOnUserType(id, $UserStore.user_type);
      }
    } catch (error) {
      isError = true;
    }
    isLoading = false;
  });
</script>

{#if !isError && !isLoading && user}
  <div class="container">
    <div class="row mt-4 pt-4">
      <div class="col-lg-4">
        <div class="card mb-2">
          <div class="card-body text-center">
            <div class="d-flex justify-content-center">
              <ProfileImage noLink={true} {user} size={80} />
            </div>
            <h5 class="mt-3">{user.full_name}</h5>
            <p class="text-muted mb-1">{user.job_title}</p>
            <!-- <p class="text-muted mb-1">{user.address}</p> -->
            <small class="text-muted mb-4">Working for the {user.location.name} office</small>
          </div>
        </div>

        <ReportTo users={user.reporting_to} />
        <!-- RFV0.1 {#if $UserStore.user_type === 'Admin' || $UserStore.user_type === 'Supervisor' || $UserStore.id === id}
            <Evaluation {user}/>
            <UserDocuments user={user} />
          {/if} -->
      </div>
      <div class="col-lg-8">
        <UserData bind:user />
        <!-- RFV0.1 <div class="row">
            <Skills bind:skills={user.skills} />
            <Certificates bind:certificates={user.user_certificates} />
          </div> -->
        {#if $UserStore.user_type === "Admin" || $UserStore.user_type === "Supervisor" || $UserStore.id === id}
          <!-- <div class="row">
            <Company bind:companies={user.user_company_properties} />
          </div> -->
          <VacationBalance {user} />
        {/if}
        <!-- RFV0.1 {#if $UserStore.user_type === 'Admin' || $UserStore.id === id}
            <div class="row">
              <Salary salaries={user.salary} />
            </div>
          {/if} -->
      </div>
    </div>
  </div>
{:else if isError}
  <div class="container height-100">
    <NotFound error={404} />
  </div>
{/if}

<style>
  :global(.icon) {
    font-size: 1.4rem;
  }
  :global(.name) {
    font-size: 1rem;
  }
</style>
