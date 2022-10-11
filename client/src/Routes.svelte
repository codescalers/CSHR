<script lang="ts">
  import { Router, Route } from 'svelte-navigator';
  import Register from './pages/Register.svelte';
  import Calendar from './pages/Calendar.svelte';
  import Notifications from './pages/Notifications.svelte';
  import Users from './pages/Users.svelte';
  import Logout from './pages/Logout.svelte';
  import Settings from './pages/Settings.svelte';
  import Login from './pages/Login.svelte';
  import { setTheme } from './services/utils/theme';
  import { onMount } from 'svelte';
  import Error from './pages/Error.svelte';
  import Requests from './pages/Requests.svelte';
  import UserProfile from './pages/UserProfile.svelte';
  import Team from './pages/Team.svelte';
  import Evaluation from './pages/Evaluation.svelte';
  import VacationBalance from './pages/VacationBalance.svelte';
  
  const mode = localStorage.getItem('mode') as 'light' | 'dark' | null;

  onMount(async () => {
    if (mode) setTheme(mode);
  });
</script>

<main>
  <Router>
    <Route path={'/'} component={Calendar} />
    <Route path="/settings"><Settings /></Route>
    <Route path={'/login'} component={Login} />
    <Route path="notifications/"><Notifications /></Route>
    <Route path="auth/register/"><Register /></Route>
    <Route path="auth/logout/"><Logout /></Route>
    <Route path="requests/"><Requests /></Route>
    <Route path="users/"><Users /></Route>
    <Route path="profile/:user_type/:id" component={UserProfile} />
    <Route path="profile/:id" component={UserProfile} />
    <Route path="profile/" component={UserProfile} />
    <Route path="team/"><Team /></Route>
    <Route path="evaluation/"><Evaluation /></Route>
    <Route path="vacation/balance/"><VacationBalance /></Route>
    <Route>
      <Error error={404} />
    </Route>
  </Router>
</main>
