<script lang="ts">
  import { Router, Route } from 'svelte-navigator';
  import Register from './pages/Register.svelte';
  import Calendar from './pages/Calendar.svelte';
  import Notifications from './pages/Notifications.svelte';
  import Users from './pages/Users.svelte';
  import InputExample from './pages/InputExample.svelte';
  import Logout from './pages/Logout.svelte';
  import Settings from './pages/Settings.svelte';
  import LoggedRoute from './routes/LoggedRoute.svelte';
  // import AdminRoute from "./routes/AdminRoute.svelte";
  // import Supervisor from './routes/Supervisor.svelte'
  import Login from './pages/Login.svelte';
  import { setTheme } from './services/utils/theme';
  import { onMount } from 'svelte';
  import Error from './pages/Error.svelte';
  import Requests from './pages/Requests.svelte';
  import UserProfile from './pages/UserProfile.svelte';
  import Team from './pages/Team.svelte';
  import Evaluation from './pages/Evaluation.svelte';
  const mode = localStorage.getItem('mode') as 'light' | 'dark' | null;

  onMount(async () => {
    if (mode) setTheme(mode);
  });
</script>

<main>
  <Router>
    <LoggedRoute path={'/'} component={Calendar} />
    <Route path="/settings"><Settings /></Route>
    <Route path={'/login'} component={Login} />
    <Route path="notifications/"><Notifications /></Route>
    <Route path="auth/register/"><Register /></Route>
    <Route path="auth/logout/"><Logout /></Route>
    <Route path="input"><InputExample /></Route>
    <Route path="requests/"><Requests /></Route>
    <Route path="users/"><Users /></Route>
    <Route path="profile/:user_type/:id" component={UserProfile} />
    <Route path="profile/:id" component={UserProfile} />
    <Route path="profile/" component={UserProfile} />
    <Route path="team/"><Team /></Route>
    <Route path="evaluation/"><Evaluation /></Route>

    <Route>
      <Error error={404} />
    </Route>
  </Router>
</main>
