<script lang="ts">
  import { Link } from 'svelte-navigator';

  import type { UserInterface } from '../../types';
  export let user: UserInterface;
</script>

<Link class="card rounded bg-light shadow" to={`../profile/${user.id}`}>
  <div class="card-body px-4 card-hover">
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
</style>
