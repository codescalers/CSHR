<script>
  import { Route , navigate} from 'svelte-navigator';
  import isAuthenticated from '../services/authentication/IsAuthenticated';
  import NotLoggedIn from '../pages/NotLoggedIn.svelte';
  import Login from '../pages/Login.svelte'
  import {authStore} from '../stores';
  import { UserStore } from '../stores';
  

  export let path;
  export let component; 
  authStore.isAuth()
  
   
</script>

{#if $UserStore !== undefined}
 
 <Route {path} {component}  />
{:else}
 
  <Route {path} component={Login} />
 
{/if}
