<script lang="ts">
  import ProfileImage from "./ProfileImage.svelte";
  export let users: any;
</script>

{#if users.length !== 0}
  <div class="card">
    <div class="card-header">Reporting to</div>
    <div class="row p-4">
      {#each users as user}
        <div class="col-2 p-0 ml-3 pl-2 mb-2 d-flex justify-content-center">
          <ProfileImage {user} />
        </div>
      {/each}
    </div>
  </div>
{/if}
