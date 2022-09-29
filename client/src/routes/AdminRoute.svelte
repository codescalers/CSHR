<script>
  import { Route } from 'svelte-routing';
  import isAuthenticated from '../services/authentication/IsAuthenticated';
  import Login from '../pages/Login.svelte';
  import parseJwt from '../services/authentication/JWTPars';
  import { authStore } from '../stores';
  import NotAnAdmin from '../pages/NotAnAdmin.svelte';

  export let path;
  export let component;

  $: isAdminAuth = authStore.isAdmin;
</script>

{#if isAdminAuth}
  <Route {path} {component} />
{:else}
  <Route {path} component={NotAnAdmin} />
{/if}
