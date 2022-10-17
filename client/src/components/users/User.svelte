<script lang="ts">
  import { Link } from 'svelte-navigator';

  import type { UserInterface } from '../../types';
  import ProfileImage from '../profile/ProfileImage.svelte';
  export let user: UserInterface;
</script>

<Link class="card b-0" to={`../profile/${user.id}`}>
  <div class="card-body px-4 card-hover">
    <h5 class="card-title">
      <div class="d-flex justify-content-center">
        <ProfileImage user={user} size={80}/>
      </div>
      <div class="text-center mt-4 mb-2 text-dark">{user.full_name}</div>
    </h5>
    <p class="w-100 text-center text-muted">
      <span>{user.job_title}</span>
      <small class="blockquote-footer">
        <cite title="Team">{user.team}</cite>
      </small><br/>
      <small>
        <cite>{user.email}</cite>
      </small>
    </p>
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
  .card{
    border: none;
    background: transparent !important;
  }
</style>
