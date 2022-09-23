<script>
    import {Route} from "svelte-routing";
    import isAuthenticated from '../services/authentication/IsAuthenticated';
    import NotLoggedIn from "../pages/NotLoggedIn.svelte";
    import { authStore } from "../stores";
 

    export let path;
    export let component;

    $: isAuth = authStore.isAuth;
    
 

</script>

{#if isAuth }
   
    <Route path={path} component={component} ></Route>
{:else}
<Route path={path} component={NotLoggedIn} />
{/if}
 