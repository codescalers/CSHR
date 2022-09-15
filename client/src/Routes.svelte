<script lang="ts">
  import { Router, Route } from "svelte-navigator";
  import Register from "./pages/Register.svelte";
  import Login from "./pages/Login.svelte";
  import Calendar from "./pages/Calendar.svelte";
  import Notifications from "./pages/Notifications.svelte";
  import Users from "./pages/Users.svelte";
  import InputExample from "./pages/InputExample.svelte";
  import Logout from "./pages/Logout.svelte";
  import Settings from "./pages/Settings.svelte";
  import { setTheme } from "./services/utils/theme";
  import isAuthenticated from "./services/authentication/IsAuthenticated";
  import { onMount } from "svelte";
  import Error from "./pages/Error.svelte";
  import { UserStore } from "./stores";
  import Requests from "./pages/Requests.svelte"
  const mode = localStorage.getItem("mode") as "light" | "dark" | null;

/*   const config = {
    headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
  };
 */
  onMount(async () => {
    if (mode) setTheme(mode);
    isAuthenticated();
    
    if (!$UserStore) {
      return {
        status: 302,
        redirect: "/login",
      };
    } else {
      return {
        status: 200,
        redirect: "/calendar",
      };
    }
  });
</script>

<main>
  <Router>
    <Route path="/" primary={false}><Calendar /></Route>
    <Route path="/settings" primary={false}><Settings /></Route>

    <Route path="auth/login/" primary={false}><Login /></Route>
    <Route path="notifications/" primary={false}><Notifications /></Route>
    <Route path="auth/register/" primary={false}><Register /></Route>
    <Route path="auth/logout/" primary={false}><Logout /></Route>
    <Route path="input" primary={false}><InputExample  /></Route>
    <Route path="requests/" primary={false}><Requests  /></Route>
    <Route path="users/" primary={false}><Users  /></Route>
   

    <Route>
      <Error error={404}  />
    </Route>
  </Router>
</main>
