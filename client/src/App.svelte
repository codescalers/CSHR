<script lang="ts">
  import { Route, Router } from "svelte-navigator";

  import Calendar from "./pages/Calendar.svelte";
  // import Compensations from "./pages/Compensations.svelte";
  // import CompensationsDetails from "./pages/CompensationsDetails.svelte";
  // import CompensationsUpdate from "./pages/CompensationsUpdate.svelte";
  import Dashboard from "./pages/Dashboard.svelte";
  import Error from "./pages/Error.svelte";
  // import HrLetter from "./pages/HrLetter.svelte";
  // import HrLetterDetails from "./pages/HrLetterDetails.svelte";
  import Login from "./pages/Login.svelte";
  import Logout from "./pages/Logout.svelte";
  import Notifications from "./pages/Notifications.svelte";
  // import OffcialDocument from "./pages/OffcialDocument.svelte";
  import Profile from "./pages/Profile.svelte";
  import Requests from "./pages/Requests.svelte";
  import Settings from "./pages/Settings.svelte";
  import Team from "./pages/Team.svelte";
  import Users from "./pages/Users.svelte";
  import VacationDetail from "./pages/VacationDetail.svelte";
  import VacationUpdate from "./pages/VacationUpdate.svelte";
  import LoggedRoute from "./routes/LoggedRoute.svelte";
</script>

<Router>
  <LoggedRoute path={"/"} component={Calendar} />
  <LoggedRoute path={"team/"} component={Team} />
  <LoggedRoute path={"requests/"} component={Requests} />
  <LoggedRoute path={"profile/:id"} component={Profile} />
  <LoggedRoute path={"profile/"} component={Profile} />
  <LoggedRoute path={"notifications/"} component={Notifications} />
  <LoggedRoute path={"vacations/:id"} component={VacationDetail} />
  <LoggedRoute path={"vacations/:id/update/"} component={VacationUpdate} />
  <LoggedRoute path={"dashboard/"} component={Dashboard} />
  <LoggedRoute path={"settings/"} component={Settings} />
  <LoggedRoute path={"users/"} component={Users} />
  <LoggedRoute path={"logout/"} component={Logout} />
  <!-- <LoggedRoute path={'hr_letters/'} component={HrLetter}/> -->
  <!-- <LoggedRoute path={'hr_letters/:id/'} component={HrLetterDetails}/>  -->
  <!-- <LoggedRoute path={'offcial-document/'} component={OffcialDocument}/> -->
  <!-- <LoggedRoute path={'compensations/'} component={Compensations}/>  -->
  <!-- <LoggedRoute path={'compensations/:id'} component={CompensationsDetails}/>  -->
  <!-- <LoggedRoute path={'compensations/:id/update'} component={CompensationsUpdate}/> -->

  <Route path={"login/"} component={Login} />
  <Route>
    <Error error={404} />
  </Route>
</Router>
