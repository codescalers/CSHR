<script lang="ts">
    import type { UserDocements } from '../../types';
    import {onMount} from "svelte";
    import UserDataService from '../../services/axios/user/UserDataService';
    export let user: any;
    let documents: UserDocements[];
    onMount(async ()=>{
      documents = await UserDataService.getUserDocuments(user.id);
    });
</script>

<div class="col-md-12 my-2">
  <div class="card mb-4 mb-md-0">
    <div class="card-header">
      Documents
    </div>
    <div class="card-body">

      {#if documents && documents.length > 0}
        <div class="row">
          <div class="col-4 text-muted mb-2">
            Name
          </div>
          <div class="col-4 text-muted mb-2">
            Status
          </div>
          <div class="col-4 d-flex text-muted mb-2 justify-content-end">
            Copy Image
          </div> 
          {#each documents as document }
            <div class="col-4">
              {document.name}
            </div>
            <div class="col-4">
              {document.status}
            </div>
            <div class="col-4 d-flex justify-content-center">
              <!-- svelte-ignore a11y-img-redundant-alt -->
              {#if document.image == null}
                ---
              {:else}
                <img class="cprop"src="{document.image}" alt="doc image">
              {/if}
            </div>
          {/each}
        </div>
      {:else}
        <div class="alert alert-light text-center p-1 mb-0">
          There are no documents yet for 
          <span class="text-primary">
            {user.full_name.split(' ')[0]}
          </span>
        </div>
      {/if}
    </div>
  </div>
</div>

<style>
  .cprop{
    width: 80px;
    height: 50px;
    border-radius: 4px;
  }
</style>