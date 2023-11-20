<script lang="ts">
  import type { CompensationType } from "../../utils/types";
  import Loading from "../ui/Loading.svelte";
  import ErrorComponent from "../error/ErrorComponent.svelte";
  import { Link } from "svelte-navigator";

  export let isLoading: boolean = false;
  export let isError: boolean = false;
  export let allUserCompensation: CompensationType[];
</script>

{#if isLoading}
  <Loading />
{:else if isError}
  <ErrorComponent />
{:else}
  <table class="table">
    <thead>
      <tr>
        <th scope="col">ID</th>
        <th scope="col">Status</th>
        <th scope="col">Approval user</th>
        <th scope="col">From date</th>
        <th scope="col">End date</th>
        <th scope="col">Action</th>
      </tr>
    </thead>
    <tbody>
      {#if allUserCompensation && allUserCompensation.length > 0}
        {#each allUserCompensation as compensation}
          <tr>
            <th scope="row">{compensation.id}</th>
            <td>{compensation.status}</td>
            <td>
              {#if compensation.approval_user}
                <a href="/profile/{compensation.approval_user.id}">
                  @{compensation.approval_user.email}
                </a>
              {:else}
                ---
              {/if}
            </td>
            <td>{compensation.from_date}</td>
            <td>{compensation.end_date}</td>
            <td>
              <Link to="/compensations/{compensation.id}" class="text-dark">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  fill="currentColor"
                  class="bi bi-eye"
                  viewBox="0 0 16 16"
                >
                  <path
                    d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"
                  />
                  <path
                    d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"
                  />
                </svg>
              </Link>
              <Link
                to="/compensations/{compensation.id}/update"
                class="text-dark"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  fill="currentColor"
                  class="bi bi-pencil"
                  viewBox="0 0 16 16"
                >
                  <path
                    d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z"
                  />
                </svg>
              </Link>
            </td>
          </tr>
        {/each}
      {/if}
    </tbody>
  </table>
{/if}
