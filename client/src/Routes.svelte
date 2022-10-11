<script lang="ts">
  import { Router, Route } from 'svelte-navigator';
  import Register from './pages/Register.svelte';
  import Calendar from './pages/Calendar.svelte';
  import Notifications from './pages/Notifications.svelte';
  import Users from './pages/Users.svelte';
 
  import Logout from './pages/Logout.svelte';
  // import Settings from './pages/Settings.svelte';
  import LoggedRoute from './routes/LoggedRoute.svelte';
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
    <!-- <Route path="/settings"><Settings /></Route> -->
    <Route path={'/login'} component={Login} />
    <LoggedRoute path={"notifications/"} component={Notifications}/>
    <LoggedRoute path={"auth/logout/"} component={Logout}/> 
    <LoggedRoute path={"requests/"} component={Requests}/> 
    <LoggedRoute path={"users/"} component={Users}/> 
    <LoggedRoute path={"profile/:user_type/:id"} component={UserProfile} />
    <LoggedRoute path={"profile/:id"} component={UserProfile} />
    <LoggedRoute path={"profile/"} component={UserProfile} />
    <LoggedRoute path={"team/"} component={Team} /> 
    <LoggedRoute path={"evaluation/"}  component={Evaluation}/> 
    <LoggedRoute path={'/register'} component={Register}/> 

    <Route>
      <Error error={404} />
    </Route>
  </Router>
</main>
