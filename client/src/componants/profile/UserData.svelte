<script lang="ts">
  import { UserStore } from "../../utils/stores";
  import type {
    AdminViewInterface,
    SupervisorViewInterface,
    UserInterface,
  } from "../../utils/types";

  export let user: AdminViewInterface | SupervisorViewInterface | UserInterface;
  const hasPermission: boolean =
    $UserStore.id == user.id ||
    $UserStore.user_type == "Admin" ||
    $UserStore.user_type == "Supervisor";
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
        <p class="mb-0">Telegram</p>
      </div>
      <div class="col-sm-9">
        <a class="text-primary mb-0" href={user.telegram_link}
          >@{user.full_name.split(" ")[0]}</a
        >
      </div>
    </div>
    <hr />
    <div class="row">
      <div class="col-sm-3">
        <p class="mb-0">Birthday</p>
      </div>
      <div class="col-sm-9">
        <p class="text-muted mb-0">{user.birthday}</p>
      </div>
    </div>
    {#if hasPermission}
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
          <p class="mb-0">Social insurance number</p>
        </div>
        <div class="col-sm-9">
          <p class="text-muted mb-0">{user.social_insurance_number}</p>
        </div>
      </div>
    {/if}
    <hr />
    <div class="row">
      <div class="col-sm-3">
        <p class="mb-0">Address</p>
      </div>
      <div class="col-sm-9">
        <p class="text-muted mb-0">{user.address}</p>
      </div>
    </div>
    <hr />
    <div class="row">
      <div class="col-sm-3">
        <p class="mb-0">Joining date</p>
      </div>
      <div class="col-sm-9">
        <p class="text-muted mb-0">{user.created_at.slice(0, 10)}</p>
      </div>
    </div>
    <hr />
    <div class="row">
      <div class="col-sm-3">
        <p class="mb-0">Location</p>
      </div>
      <div class="col-sm-9">
        <p class="text-primary mb-0">{user.location.name}</p>
      </div>
    </div>
  </div>
</div>
