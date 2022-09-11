<script lang="ts">
  import { UserStore } from "../../stores";
  import Modal from "../modal/Modal.svelte";
  import StackedImages from "../image/StackedImages.svelte";

  export let item: any;
  console.table(item);
</script>

<Modal
  bind:id={item.id}
  isDelete={false}
  isDone={false}
  doneText={""}
  on:onDelete
  on:onDone
  deleteText={""}
  isFooter={true}
>
  <div slot="header">
    <h6 class="modal-title" id="exampleModalLongTitle">
      {item.title.toUpperCase()}
    </h6>
  </div>
  <div slot="body">
    <div class="container d-flex flex-column gap-5 px-5 my-5 mx-xl-4">
      <div class="row">
        <h5>Organizer</h5>
        <div class="d-flex flex-column gap-2">
          <div class="d-flex flex-row gap-2">
            <div class="d-flex flex-column gap-1">
              <span class="text-muted">Full Name : </span>
              <span class="text-muted">Team : </span>
              <span class="text-muted">Email :</span>
            </div>
            <div class="d-flex flex-column gap-1">
              <span>{item.host_user.full_name}</span>
              <span>{item.host_user.team}</span>
              <span
                ><a
                  href={`mailto:${item.host_user.email}?subject=Happy%20Birth%20Day%20ahmad&body=Dear%20${item.host_user.full_name}%2C%0D%0A%0D%0AI%20wish%20you%20a%20happy%20birthday%20${item.host_user.full_name}%F0%9F%8E%82%0D%0A%0D%0A%0D%0Ayour%20beloved%2C%0D%0A${$UserStore.full_name}`}
                  >{item.host_user.email}
                </a></span
              >
            </div>
          </div>
          <div class="my-2 right">
            <a
              href={`mailto:${item.host_user.email}?subject=Happy%20Birth%20Day%20ahmad&body=Dear%20${item.host_user.full_name}%2C%0D%0A%0D%0AI%20wish%20you%20a%20happy%20birthday%20${item.host_user.full_name}%F0%9F%8E%82%0D%0A%0D%0A%0D%0Ayour%20beloved%2C%0D%0A${$UserStore.full_name}`}
            >
              <button class="btn btn-outline-primary">
                send a message</button
              ></a
            >
          </div>
          <hr />
        </div>
      </div>
      <div class="row">
        <h5>Particpants</h5>
      </div>
      <StackedImages stackedImages={[...item.invited_users]} />
      <div class="d-flex flex-column gap-2">
        {#each item.invited_users as user, index (index)}
          <div class="d-flex flex-row gap-2">
            <div class="d-flex flex-column gap-1">
              <span class="text-muted">Full Name : </span>
              <span class="text-muted">Team : </span>
              <span class="text-muted">Email :</span>
            </div>
            <div class="d-flex flex-column gap-1">
              <span>{user.full_name}</span>
              <span>{user.team}</span>
              <span
                ><a
                  href={`mailto:${user.email}?subject=Happy%20Birth%20Day%20ahmad&body=Dear%20${user.full_name}%2C%0D%0A%0D%0AI%20wish%20you%20a%20happy%20birthday%20${user.full_name}%F0%9F%8E%82%0D%0A%0D%0A%0D%0Ayour%20beloved%2C%0D%0A${$UserStore.full_name}`}
                  >{user.email}
                </a></span
              >
            </div>
          </div>
          <div class="my-2 right">
            <a
              href={`mailto:${user.email}?subject=Happy%20Birth%20Day%20ahmad&body=Dear%20${user.full_name}%2C%0D%0A%0D%0AI%20wish%20you%20a%20happy%20birthday%20${user.full_name}%F0%9F%8E%82%0D%0A%0D%0A%0D%0Ayour%20beloved%2C%0D%0A${$UserStore.full_name}`}
            >
              <button class="btn btn-outline-primary">
                send a message</button
              ></a
            >
          </div>
          {#if index != item.invited_users?.length - 1}
            <hr />
          {/if}
        {/each}
      </div>
    </div>
  </div>
</Modal>

<style>
  .right {
    margin-left: auto;
    margin-right: 0;
  }
</style>
