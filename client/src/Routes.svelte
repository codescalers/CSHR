<script lang="ts">
  import { Router, Route } from "svelte-navigator";
  import Register from "./pages/Register.svelte";
  import Login from "./pages/Login.svelte";
  import type { UserInterface } from "./types";
  import Calendar from "./pages/Calendar.svelte";
  import Notifications from "./pages/Notifications.svelte";
  import InputExample from "./pages/InputExample.svelte";
  import Logout from "./pages/Logout.svelte";
  import Settings from "./pages/Settings.svelte";
  import { setTheme } from "./services/utils/theme";
  import isAuthenticated from "./services/authentication/IsAuthenticated";
  import { onMount } from "svelte";
  import Error from "./pages/Error.svelte";
  import axios from "axios";
  let user: UserInterface;
  const mode = localStorage.getItem("mode") as "light" | "dark" | null;

  const config = {
    headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
  };

  onMount(async () => {
    if (mode) setTheme(mode);
    isAuthenticated();
    const userDetails = await axios.get("/dashboard/user/", config);
    user = await userDetails.data.data;
    if (!user) {
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
    <Route path="/" primary={true}><Calendar {user} /></Route>
    <Route path="/settings" primary={false}><Settings {user} /></Route>

    <Route path="auth/login/" primary={false}><Login /></Route>
    <Route path="notifications/" primary={false}><Notifications {user} /></Route
    >
    <Route path="auth/register/" primary={false}><Register /></Route>
    <Route path="auth/logout/" primary={false}><Logout /></Route>
    <Route path="input" primary={false}><InputExample {user} /></Route>

    <Route>
      <Error error={404} {user} />
    </Route>
  </Router>
</main>
