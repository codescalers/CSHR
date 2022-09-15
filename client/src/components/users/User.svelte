<script lang="ts">
  import type { UserInterface } from "../../types";
  export let user: UserInterface;
</script>

<div class="card rounded">
  <div class="card-body">
    <h5 class="card-title">
      <div
        class={`circular_img my-2  mx-auto`}
        style={`background-image:url(${
          process.env.APP_BASE_API_URL + user.image
        });background-color:${
          user.gender === "Male" ? "#2986cc" : "#FB5858"
        };border:1.5px solid ${
          user.gender === "Male" ? "var(--secondary-color)" : "pink"
        }`}
        data-bs-toggle="tooltip"
        title={user.full_name + " #" + user.team}
      />
      <span> {user.full_name} </span>
    </h5>
    <p class="card-text">
      Some quick example text to build on the card title and make up the bulk of
      the card's content.
    </p>
    <a href="#" class="btn btn-primary">visit profile</a>
  </div>
</div>

<style>
  :global(.circular_img) {
    width: 4.7rem;
    height: 4.7rem;
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
