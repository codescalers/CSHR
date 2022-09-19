<script lang="ts">
  import Members from "./Members.svelte";
  import Supervisors from "./Supervisors.svelte";
</script>

<div class="container">
  <div class="row">
    <div class="col-12">
      <h4>Supervisors</h4>
    </div>
    <div class="col-12">
      <Supervisors />
    </div>
  </div>
  <div class="row">
    <div class="col-12">
      <h4>Members</h4>
    </div>
    <div class="col-12">
      <Members />
    </div>
  </div>
</div>
