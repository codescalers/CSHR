<script>
    import {Route} from "svelte-routing";
    import isAuthenticated from '../services/authentication/IsAuthenticated';
    import Login from "../pages/Login.svelte"
  import parseJwt from "../services/authentication/JWTPars";
  import { UserStore } from "../stores";
  import NotAnAdmin from "../pages/NotAnAdmin.svelte";
 

    export let path;
    export let component;
    const isAdmin = ($UserStore.user_type=="Admin")


    $: isAdminAuth  =  isAuthenticated() && isAdmin
    
</script>


{#if isAdminAuth }
    <Route path={path} component={component} ></Route>
{:else}
<Route path={path} component={NotAnAdmin} />
{/if}
 