<script lang="ts">
    import ProfileImage from "./ProfileImage.svelte";
    export let users: any; 
</script>
      
    <div class="card">
        <div class="card-header">
            Reporting to
        </div>
        {#if users.length === 0}
            <span class="text-primary text-center p-3">
                Reporting to, nobody.
            </span>
        {:else}
            <div class="row p-2">
                {#each users as user }
                    <div class="col-2 p-0 ml-3 pl-2 mb-2 d-flex justify-content-center">
                        <ProfileImage user={user} />
                    </div>
                    <div class="col-9 p-0 d-flex align-items-center">
                        <p>{user.full_name}</p>
                    </div>
                {/each}
            </div>
        {/if}
    </div>