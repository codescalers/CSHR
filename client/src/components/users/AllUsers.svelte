<script lang="ts">
  import type { UserInterface } from "../../types";
  import User from "./User.svelte";
  export let users: UserInterface[];
</script>

<div class="container">
  <h1>All Users</h1>

  <div class="row row-cols-lg-3 row-cols-2 gy-2">
    <div class="col">
      {#each users as user (user.id)}
        <User {user} />
      {/each}
    </div>
  </div>
</div>
