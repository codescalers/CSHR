<script lang="ts">
  import type {
    AdminViewInterface,
    SupervisorViewInterface,
    UserInterface,
  } from '../../types';
  import { onMount } from 'svelte';
  import { useParams } from 'svelte-navigator';
  import { UserStore } from '../../stores';
  import usersDataService from '../../services/axios/users/UsersDataService';
  import Skills from './Skills.svelte';
  import Certificates from './Certificates.svelte';
  import UserData from './UserData.svelte';
  import Evaluation from './Evaluation.svelte';
  import Company from './Company.svelte';
  import Salary from './Salary.svelte';
  import ProfileImage from './ProfileImage.svelte';
  import ReportTo from './ReportTo.svelte';
  import UserDocuments from './GetUserDocuments.svelte';
  import VacationBalance from './VacationBalance.svelte';

  const params = useParams();
  let id: number = Number($params.id);

  export let isLoading = false;
  export let isError: boolean | null = null;
  let user:
    | AdminViewInterface
    | SupervisorViewInterface
    | UserInterface
    | null = null;
  onMount(async () => {
    isLoading = true;
    try {
      if ($UserStore !== undefined && $UserStore.id === id) {
        user = $UserStore;
      } else {
        user = await usersDataService.getById(id, $UserStore.user_type);
      }
    } catch (error) {
      isError = true;
    }
    isLoading = false;
  });
</script>

{#if !isError && !isLoading && user}
  <div class="container ">
    <div class="row">
      <div class="col-lg-4">
        <div class="card mb-4">
          <div class="card-body text-center">
            <div class="d-flex justify-content-center">
              <ProfileImage user={user} size={80}/>
            </div>
            <h5 class="my-3">{user.full_name}</h5>
            <p class="text-muted mb-1">{user.job_title}</p>
            <p class="text-muted mb-4">{user.address}</p>
          </div>
        </div>

        <ReportTo users={user.reporting_to}/>
        {#if $UserStore.user_type === 'Admin' || $UserStore.user_type === 'Supervisor' || $UserStore.id === id}
          <Evaluation {user}/>
          <UserDocuments user={user} />
        {/if}
      </div>
      <div class="col-lg-8">
        <UserData bind:user />
        <div class="row">
          <Skills bind:skills={user.skills} />
          <Certificates bind:certificates={user.user_certificates} />
        </div>
        {#if $UserStore.user_type === 'Admin' || $UserStore.user_type === 'Supervisor' || $UserStore.id === id}
          <div class="row">
            <Company bind:companies={user.user_company_properties} />
          </div>
          <VacationBalance user={user}/>
        {/if}
        {#if $UserStore.user_type === 'Admin' || $UserStore.id === id}
          <div class="row">
            <Salary salaries={user.salary} />
          </div>
        {/if}
      </div>
    </div>
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
