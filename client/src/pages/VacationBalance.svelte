<script lang="ts">
    import Sidebar from '../components/sidebar/Sidebar.svelte';
    import AdminBalance from '../components/vacations/AdminBalance.svelte';
    import { UserStore } from '../stores';
    export let isLoading = false;
    export let isError: boolean | null = null;

    let user = UserStore
</script>

<Sidebar bind:isLoading bind:isError>
    <span slot="page-name">Update vacation balance</span>
    <div class="container mt-4" slot="content">
        <!-- Tabs navs -->
<ul class="nav nav-tabs mb-3" id="ex1" role="tablist">
    <li class="nav-item" role="presentation">
      <a
        class="nav-link active"
        id="ex1-tab-1"
        data-mdb-toggle="tab"
        href="#ex1-tabs-1"
        role="tab"
        aria-controls="ex1-tabs-1"
        aria-selected="true"
        >Tab 1</a
      >
    </li>
    <li class="nav-item" role="presentation">
      <a
        class="nav-link"
        id="ex1-tab-2"
        data-mdb-toggle="tab"
        href="#ex1-tabs-2"
        role="tab"
        aria-controls="ex1-tabs-2"
        aria-selected="false"
        >Tab 2</a
      >
    </li>
    <li class="nav-item" role="presentation">
      <a
        class="nav-link"
        id="ex1-tab-3"
        data-mdb-toggle="tab"
        href="#ex1-tabs-3"
        role="tab"
        aria-controls="ex1-tabs-3"
        aria-selected="false"
        >Tab 3</a
      >
    </li>
  </ul>
  <!-- Tabs navs -->
  
  <!-- Tabs content -->
  <div class="tab-content" id="ex1-content">
    <div
      class="tab-pane fade show active"
      id="ex1-tabs-1"
      role="tabpanel"
      aria-labelledby="ex1-tab-1"
    >
      Tab 1 content
    </div>
    <div class="tab-pane fade" id="ex1-tabs-2" role="tabpanel" aria-labelledby="ex1-tab-2">
      Tab 2 content
    </div>
    <div class="tab-pane fade" id="ex1-tabs-3" role="tabpanel" aria-labelledby="ex1-tab-3">
      Tab 3 content
    </div>
  </div>
  <!-- Tabs content -->
        <AdminBalance user={$user}/>
    </div>
</Sidebar>