<script lang="ts">
  // import UpdateProfile from "./UpdateProfile.svelte"
  import ChangePassword from "./ChangePassword.svelte"
  // import { UserStore } from "../../utils/stores"
  // import AddtionalInfo from "./AddtionalInfo.svelte";
</script>

<div class="container mt-5 pt-5 height-100">
  <div class="card p-2 mb-3">
    <ul class="nav mt-4 nav-tabs nav-fill mb-3" id="ex1" role="tablist">
      <!-- <li RFNV1.0 class="nav-item" role="presentation">
        <a
          class="nav-link navlink active"
          id="ex2-tab-1"
          data-mdb-toggle="tab"
          href="#ex2-tabs-1"
          role="tab"
          aria-controls="ex2-tabs-1"
          aria-selected="true"
          >Update Profile</a
        >
      </li> -->
      <li class="nav-item" role="presentation">
        <a
          class="nav-link navlink active"
          id="ex2-tab-2"
          data-mdb-toggle="tab"
          href="#ex2-tabs-2"
          role="tab"
          aria-controls="ex2-tabs-2"
          aria-selected="false"
          >Change Password</a
        >
      </li>
      <!-- <li RFNV1.0 class="nav-item" role="presentation">
        <a
          class="nav-link navlink"
          id="ex2-tab-2"
          data-mdb-toggle="tab"
          href="#ex2-tabs-3"
          role="tab"
          aria-controls="ex2-tabs-3"
          aria-selected="false"
          >Additional information</a
        >
      </li> -->
    </ul>
  </div>
  <div class="tab-content" id="ex2-content">
    <!-- <div
      class="tab-pane show active"
      id="ex2-tabs-1"
      role="tabpanel"
      aria-labelledby="ex2-tab-1"
    >
      <UpdateProfile user={$UserStore}/>
    </div> -->
    <div
      class="tab-pane show active"
      id="ex2-tabs-2"
      role="tabpanel"
      aria-labelledby="ex2-tab-2"
    >
      <ChangePassword />
    </div>
    <!-- RFNV1.0 <div
      class="tab-pane"
      id="ex2-tabs-3"
      role="tabpanel"
      aria-labelledby="ex2-tab-3"
    >
      <AddtionalInfo />
    </div> -->
  </div>
</div>



<style>
  .nav {
      height: 100%;
      display: flex;
      flex-direction: row;
      justify-content: space-between;
      overflow: hidden;
      border-bottom: none !important;
  }
  .navlink{
    padding: 15px;
    border-radius: 5px !important;
  }
</style>