<script lang="ts">
  import type {
    AdminViewInterface,
    SupervisorViewInterface,
    UserInterface,
  } from '../../types';

  export let user: AdminViewInterface | SupervisorViewInterface | UserInterface;
</script>

<div class="card mb-4">
  <div class="card-body">
    <div class="row">
      <div class="col-sm-3">
        <p class="mb-0">Full Name</p>
      </div>
      <div class="col-sm-9">
        <p class="text-muted mb-0">{user.full_name}</p>
      </div>
    </div>
    <hr />
    <div class="row">
      <div class="col-sm-3">
        <p class="mb-0">Email</p>
      </div>
      <div class="col-sm-9">
        <p class="text-muted mb-0">{user.email}</p>
      </div>
    </div>
    <hr />
    <div class="row">
      <div class="col-sm-3">
        <p class="mb-0">Team</p>
      </div>
      <div class="col-sm-9">
        <p class="text-muted mb-0">{user.team}</p>
      </div>
    </div>
    <hr />
    <div class="row">
      <div class="col-sm-3">
        <p class="mb-0">Phone Number</p>
      </div>
      <div class="col-sm-9">
        <p class="text-muted mb-0">{user.mobile_number}</p>
      </div>
    </div>
    <hr />
    <div class="row">
      <div class="col-sm-3">
        <p class="mb-0">Address</p>
      </div>
      <div class="col-sm-9">
        <p class="text-muted mb-0">{user.address}</p>
      </div>
    </div>
  </div>
</div>
