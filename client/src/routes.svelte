<script lang="ts">
  import { Router, Route } from "svelte-navigator";
  import Register from "./pages/Register.svelte";
  import Login from "./pages/Login.svelte";
  import type { UserInterface } from "./types";
  import Calendar from "./pages/Calender.svelte";
  import Logout from "./pages/Logout.svelte";


  import { onMount } from "svelte";
  import Error from "./pages/Error.svelte";
  let user: UserInterface;
  const mode = localStorage.getItem("mode");

  const config = {
    headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
  };
  onMount(async () => {
    setTheme(mode);
    isAuthenticated();
    const userDetails = await axios.get("/dashboard/user/", config);
    user = await userDetails.data.data;
    if (!user) {
      return {
        status: 302,
        redirect: "/login",
      };
    }
  });
</script>

<main>
  <Router>
    <Route path="/" primary={false}><Calendar {user} /></Route>
    <Route path="settings/" primary={false}><Settings {user} /></Route>

    <Route path="auth/login/" primary={false}><Login /></Route>
    <Route path="auth/register/" primary={false}><Register /></Route>
    <Route path="auth/logout/" primary={false}><Logout /></Route>

    <Route path="projects/" primary={false}><Projects {user} /></Route>
    <Route path="projects/:id/" primary={false}><ProjectDetails {user} /></Route
    >
    <Route path="projects/:id/update/" primary={false}
      ><UpdateProject {user} /></Route
    >

    <Route path="projects/:id/test-plans/" primary={false}
      ><TestPlans {user} /></Route
    >
    <Route path="projects/:id/test-plans/:id/" primary={false}
      ><TestPlanDetails {user} /></Route
    >

    <Route path="projects/:id/requirements/" primary={false}
      ><Requirements {user} /></Route
    >
    <Route path="projects/:id/requirements/:id/" primary={false}
      ><RequirementsDetails {user} /></Route
    >

    <Route path="projects/:id/test-suites/" primary={false}
      ><TestSuite {user} /></Route
    >
    <Route path="projects/:id/test-suites/:id/" primary={false}
      ><TestSuiteDetails {user} /></Route
    >

    <Route path="members/" primary={false}><Members {user} /></Route>
    <Route path="members/:id/" primary={false}><MemberDetails {user} /></Route>

    <Route path="projects/:id/runs/" primary={false}><TestRun {user} /></Route>
    <Route path="projects/:id/runs/:id/" primary={false}
      ><TestRunDeetails {user} /></Route
    >
    <Route path="projects/:id/runs/:id/run" primary={false}
      ><RunTestRun {user} /></Route
    >

    <Route>
      <Error error={404} />
    </Route>
  </Router>
</main>
