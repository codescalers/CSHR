<script>
  import { Route } from 'svelte-routing';
  import isAuthenticated from '../services/authentication/IsAuthenticated';
  import NotLoggedIn from '../pages/NotLoggedIn.svelte';
  import { authStore } from '../stores';

  export let path;
  export let component;

  $: isAuth = authStore.isAuth;
</script>

{#if isAuth}
  <Route {path} {component} />
{:else}
  <Route {path} component={NotLoggedIn} />
{/if}
