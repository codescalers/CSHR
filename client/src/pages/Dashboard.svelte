<script lang="ts">
  import { Route } from "svelte-navigator";
  import { UserStore } from "../utils/stores";
  import Error from "./Error.svelte";
  import Sidebar from "../componants/sidebar/Sidebar.svelte";
  import Tabs from "../componants/dashboard/Tabs.svelte";
</script>

{#if $UserStore.user_type != "Admin"}
  <Route>
    <Error error={404} />
  </Route>
{:else}
  <Sidebar>
    <section slot="content">
      <Tabs />
    </section>
  </Sidebar>
{/if}
