<script lang="ts">
  import { Link } from 'svelte-navigator'

  import type { UserInterface } from '../../types'
  export let user: UserInterface
</script>

<div class="card rounded bg-light shadow">
  <div class="card-body px-4">
    <h5 class="card-title">
      <div
        class={`my-2  mx-auto card-img-top circular_img`}
        style={`background-image:url(${
          process.env.APP_BASE_API_URL + user.image
        });background-color:${
          user.gender === 'Male' ? '#2986cc' : '#FB5858'
        };border:1.5px solid ${
          user.gender === 'Male' ? 'var(--secondary-color)' : 'pink'
        }`}
        data-bs-toggle="tooltip"
        title={user.full_name + ' #' + user.team}
      />
      <div class="text-center my-4 mx-3">{user.full_name}</div>
    </h5>
    <p class="card-text" />
    <p class="blockquote-footer w-100 text-center">
      <small>
        <cite title="Team"># {user.team}</cite>
      </small>
      <br />
      <small>
        <cite title="Address">
          <i class="bi bi-geo" />
          {user.address}</cite
        >
      </small>
    </p>
    <blockquote class="blockquote mb-0">
      <p class="text-center">
        {user.job_title}
      </p>
    </blockquote>
    <div class=" d-flex flex-row justify-content-center gap-3 my-3">
      <a href="#" class="btn btn-primary">send email</a>
      <Link to={`../profile/${user.id}`} class="btn btn-outline-primary"
        >visit profile</Link
      >
    </div>
  </div>
</div>

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
</style>
