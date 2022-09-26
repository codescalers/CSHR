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
            <div
              class={`my-2  mx-auto card-img-top circular_img`}
              style={`background-image:url(${
                process.env.APP_BASE_API_URL + user.image
              });background-color:${
                user.gender === 'Male' ? '#2986cc' : '#FB5858'
              };border:1.5px solid ${
                user.gender === 'Male' ? 'var(--secondary-color)' : 'pink'
              }`}
              data-bs-toggle="tooltip"
              title={user.full_name + ' #' + user.team}
            />

            <h5 class="my-3">{user.full_name}</h5>
            <p class="text-muted mb-1">{user.job_title}</p>
            <p class="text-muted mb-4">{user.address}</p>
          </div>
        </div>

        <div class="card mb-4 mb-lg-0">
          <div class="card-body p-0">
            <ul class="list-group list-group-flush rounded-3">
              <li
                class="list-group-item d-flex justify-content-between align-items-center p-3"
              >
                <i class="bi bi-telegram icon" style="color:#27A1E0;" />
                <a class="mb-0" href={user.telegram_link}>telegram</a>
              </li>
            </ul>
          </div>
        </div>
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
            <Evaluation bind:evaluations={user.user_evaluation} />
          </div>
        {/if}

        {#if $UserStore.user_type === 'Admin' || $UserStore.id === id}
          <div class="row">
            <Salary bind:salaries={user.salary} />
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
