<script>
  import { Route } from "svelte-navigator";
  import Login from "../pages/Login.svelte";
  import { authStore } from "../utils/stores";
  import { UserStore } from "../utils/stores";

  export let path;
  export let component;
  authStore.isAuth();
</script>

{#if $UserStore !== undefined}
  <Route {path} {component} />
{:else}
  <Route {path} component={Login} />
{/if}
