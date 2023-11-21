<script lang="ts">
  import { Link } from "svelte-navigator";

  import type { GeneralUserInterface } from "../../utils/types";
  import ProfileImage from "../profile/ProfileImage.svelte";
  export let user: GeneralUserInterface;
</script>

<Link to={`../profile/${user.id}`}>
  <div class="card b-0 {!user.is_active ? 'inactive-bg' : 'active-bg'}">
    <div class="card-body px-4 card-hover">
      <h5 class="card-title">
        <div class="d-flex justify-content-center">
          <ProfileImage {user} size={80} />
        </div>
        <div class="text-center mt-4 mb-2 text-dark">{user.full_name}</div>
      </h5>
      {#if !user.is_active}
        <p class="w-100 text-center text-danger mb-0">inactive user</p>
      {/if}
      <p class="w-100 text-center text-muted">
        <span>{user.job_title}</span>
        <small class="blockquote-footer">
          <cite title="Team">{user.team}</cite>
        </small>
        <br />
        <small>
          <cite>{user.email}</cite>
          <br />
          <cite>{user.location.country}</cite>
        </small>
      </p>
    </div>
  </div>
</Link>

<style>
  :global(.circular_img) {
    width: 6.7rem !important;
    height: 6.7rem !important;
    border-radius: 50%;
    overflow: hidden;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    font-size: 1.7rem;
    font-weight: 700;
    letter-spacing: -0.1rem;
    text-align: center;
  }

  .card-hover:hover {
    box-shadow: 0 0 0 0.3rem var(--secondary-color);
    transform: scale(1.01);
    border-radius: inherit;
  }
  .card {
    height: 280px;
    padding: 15px;
    border: 1px solid #5526;
    border-radius: 4px;
  }
  .inactive-bg {
    background: rgba(243, 156, 156, 0.342) !important;
  }
  .active-bg {
    background: rgba(230, 222, 222, 0.342) !important;
  }
</style>
