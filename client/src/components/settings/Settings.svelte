<script lang="ts">
  import UpdateProfile from "./UpdateProfile.svelte"
  import ChangePassword from "./ChangePassword.svelte"
  import { UserStore } from "../../stores"
  import AddtionalInfo from "./AddtionalInfo.svelte";
</script>

<div class="container">
  <ul class="nav mt-4 nav-tabs nav-fill mb-3" id="ex1" role="tablist">
    <li class="nav-item" role="presentation">
      <a
        class="nav-link active"
        id="ex2-tab-1"
        data-mdb-toggle="tab"
        href="#ex2-tabs-1"
        role="tab"
        aria-controls="ex2-tabs-1"
        aria-selected="true"
        >Update Profile</a
      >
    </li>
    <li class="nav-item" role="presentation">
      <a
        class="nav-link"
        id="ex2-tab-2"
        data-mdb-toggle="tab"
        href="#ex2-tabs-2"
        role="tab"
        aria-controls="ex2-tabs-2"
        aria-selected="false"
        >Change Password</a
      >
    </li>
    <li class="nav-item" role="presentation">
      <a
        class="nav-link"
        id="ex2-tab-2"
        data-mdb-toggle="tab"
        href="#ex2-tabs-3"
        role="tab"
        aria-controls="ex2-tabs-3"
        aria-selected="false"
        >Additional information</a
      >
    </li>
  </ul>
  <div class="tab-content" id="ex2-content">
    <div
      class="tab-pane show active"
      id="ex2-tabs-1"
      role="tabpanel"
      aria-labelledby="ex2-tab-1"
    >
      <UpdateProfile user={$UserStore}/>
    </div>
    <div
      class="tab-pane"
      id="ex2-tabs-2"
      role="tabpanel"
      aria-labelledby="ex2-tab-2"
    >
      <ChangePassword />
    </div>
    <div
      class="tab-pane"
      id="ex2-tabs-3"
      role="tabpanel"
      aria-labelledby="ex2-tab-3"
    >
      <AddtionalInfo />
    </div>
  </div>
</div>



<style>
  .nav {
      height: 100%;
      display: flex;
      flex-direction: row;
      justify-content: space-between;
      overflow: hidden;
  }
</style>