<script lang="ts">
  import Users from "../../apis/users/users";
  import type { SelectOptionsComponent, UserInterface } from "../../utils/types";
  import Submit from "../ui/Button.svelte";
  import PeopleSelect from "../ui/select/UsersMultiSelect.svelte";
  import UpdateUserProfileForm from "./Forms/UpdateUserProfileForm.svelte";

  export let isLoading = false;

  let isUserLoaded = false;
  let user: UserInterface;
  $: submitDisabled = usersOptions.selected.length == 0;

  async function loadUserBalance() {
    const userID = usersOptions.selected[0].value;
    const _user: UserInterface = await Users.getUserByID(userID);
    if (_user) {
      user = _user;
      isUserLoaded = true;
    }
  }

  let successMessage: string;
  let errorMessage: string;

  let usersOptions: SelectOptionsComponent = {
    optionsList: [],
    label: "User",
    placeholder: "Select User...",
    selected: [],
    isTop: true,
    multiple: false,
  };

  function watchUser() {
    if (isUserLoaded && !user) {
      isUserLoaded = null;
    }
  }

  $: user, watchUser();
</script>

{#if !user}
  <div class="card">
    <div class="card-body">
      <div class="row">
        {#if !isUserLoaded}
          <PeopleSelect bind:options={usersOptions} usersInAdminOffice={true} />
          <div class="col-12">
            <div class="form-outline mt-4 d-flex justify-content-center">
              <Submit
                width={"25"}
                bind:successMessage
                bind:errorMessage
                label="Load User"
                onClick={async () => {
                  isLoading = true;
                  await loadUserBalance();
                  isLoading = false;
                  return usersOptions.isError;
                }}
                className=""
                bind:disabled={submitDisabled}
              />
            </div>
          </div>
        {/if}
      </div>
    </div>
  </div>
{:else}
  <UpdateUserProfileForm bind:user bind:isUserLoaded />
{/if}
