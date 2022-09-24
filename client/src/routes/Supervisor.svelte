<script>
  import { Route } from 'svelte-routing';
  import isAuthenticated from '../services/authentication/IsAuthenticated';
  import Login from '../pages/Login.svelte';
  import parseJwt from '../services/authentication/JWTPars';
  import NotAnAdmin from '../pages/NotAnAdmin.svelte';
  import { authStore } from '../stores';

  export let path;
  export let component;

  $: isSuperAuth = authStore.isSupervisor;
</script>

{#if isSuperAuth}
  <Route {path} {component} />
{:else}
  <Route {path} component={NotAnAdmin} />
{/if}
