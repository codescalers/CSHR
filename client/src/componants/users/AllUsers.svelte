<script lang="ts">
  import { onMount } from "svelte";

  import officeDataService from "../../apis/offices/Office";
  import usersDataService from "../../apis/users/users";
  import { OfficeStore, UserStore } from "../../utils/stores";
  import type {
    OfficeType,
    SelectOptionsComponent,
    SelectOptionType,
    UserInterface
  } from "../../utils/types";
  import Loading from "../ui/Loading.svelte";
  import MultiSelect from "../ui/select/MultiSelect.svelte";
  import User from "./User.svelte";

  export let isLoading = false;
  export let isError: boolean | null = null;

  let users: UserInterface[];
  let userOffice = $UserStore.location;
  let isLoadingUsers = false;

  const changeOffice = (selectedOffice: SelectOptionType) => {
    const office = $OfficeStore.filter(
      (_office: OfficeType) => _office.id === selectedOffice.value
    )[0]; // Value is the id.
    if (userOffice.id != office.id) {
      userOffice = office;
      loadUsers();
    }
  };

  const loadUsers = async () => {
    isLoadingUsers = true;
    options.disabled = true;
    users = await usersDataService.getAll({ locationId: userOffice.id });
    options.disabled = false;
    isLoadingUsers = false;
  };

  onMount(async () => {
    isLoading = true;
    try {
      if ($OfficeStore === undefined || $OfficeStore.length === 0) {
        const offices = await officeDataService.getAll();
        if ($OfficeStore === undefined) {
          $OfficeStore = offices;
        } else {
          OfficeStore.set(offices);
        }
      }
      $OfficeStore.forEach((office: OfficeType) => {
        if (office.id === userOffice.id) {
          locationSelected.push({
            value: office.id,
            label: office.name
          });
        }
        locationOptions.push({
          value: office.id,
          label: office.name
        });
      });
      loadUsers();
    } catch (error) {
      isError = true;
    }
    isLoading = false;
  });

  let locationOptions: SelectOptionType[] = [];
  let locationSelected: SelectOptionType[] = [];
  let isErrorLocation: undefined | boolean;

  let options: SelectOptionsComponent = {
    optionsList: locationOptions,
    selected: locationSelected,
    isLabel: true,
    label: "Select Office",
    placeholder: "Select Office.",
    multiple: false,
    isError: isErrorLocation,
    isTop: true
  };
</script>

{#if isLoading}
  <div class="height-100 d-flex justify-content-center align-items-center">
    <Loading className={"loader"} />
  </div>
{:else if !isLoading && !isError && users}
  <div class="container">
    <div class="card office-selection" style="margin-top: 15px;">
      <small>
        You can change the selected office to discover the team in other
        offices, current elected office is your office.
      </small>
      <MultiSelect
        bind:options
        on:select={(e) => changeOffice(e.detail.selected)}
      />
    </div>
    {#if isLoadingUsers}
      <div class="mt-5 d-flex justify-content-center align-items-center">
        <Loading className={"loader"} />
      </div>
    {:else if users.length}
      <div class="d-flex flex-column justify-content-between">
        <div>
          <div class="row justify-content-between">
            {#each users as user}
              <div class="col-12 col-md-6 col-lg-4 my-4">
                <User bind:user />
              </div>
            {/each}
          </div>
        </div>
      </div>
    {:else}
      <div class="d-flex justify-content-center align-items-center">
        <div class="alert alert-warning">
          It appears that there are no users in this office
        </div>
      </div>
    {/if}
  </div>
{/if}

<style scoped>
  .office-selection {
    margin-top: 100px !important;
    margin-bottom: 16px;
    padding: 15px;
  }
</style>
