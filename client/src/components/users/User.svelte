<script lang="ts">
  import type { UserInterface } from "../../types";
  export let user: UserInterface;
</script>

<div class="card">
  <div class="card-body">
    <h5 class="card-title">{user.full_name}</h5>
    <p class="card-text">
      Some quick example text to build on the card title and make up the bulk of
      the card's content.
    </p>
    <a href="#" class="btn btn-primary">visit profile</a>
  </div>
</div>
