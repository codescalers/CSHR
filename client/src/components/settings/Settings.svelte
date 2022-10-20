<script lang="ts">
  import UpdateProfile from "./UpdateProfile.svelte"
  import ChangePassword from "./ChangePassword.svelte"
  import { UserStore } from "../../stores"
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
  </ul>
  <div class="tab-content" id="ex2-content">
    <div
      class="tab-pane fade show active"
      id="ex2-tabs-1"
      role="tabpanel"
      aria-labelledby="ex2-tab-1"
    >
      <UpdateProfile user={$UserStore}/>
    </div>
    <div
      class="tab-pane fade"
      id="ex2-tabs-2"
      role="tabpanel"
      aria-labelledby="ex2-tab-2"
    >
      <ChangePassword />
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