<script lang="ts">
  import type {
    meetingItemType,
    userType,
  } from "../../services/axios/home/types";
  import { UserStore } from "../../stores";
  import Modal from "../modal/Modal.svelte";
  import StackedImages from "../image/StackedImages.svelte";

  export let item: meetingItemType;
  let clickedParticipantIndex: number = 0;
  let clickedParticipantUser: userType =
    item.invited_users[clickedParticipantIndex];
  $: clickedParticipantUser = item.invited_users[clickedParticipantIndex];
  
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
    <div class="container d-flex flex-column gap-5 px-5 my-5">
      <h3 class="mx-auto text-muted">
        <a href={item.meeting_link}>Meeting Link</a>
      </h3>
      <div class="row">
        <h5>Organizer</h5>
      </div>
      <StackedImages stackedImages={[item.host_user]} />

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
        {#if Number($UserStore.id) !== Number(item.id)}
          <div class="my-2 right">
            <a
              href={`mailto:${item.host_user.email}?subject=Happy%20Birth%20Day%20ahmad&body=Dear%20${item.host_user.full_name}%2C%0D%0A%0D%0AI%20wish%20you%20a%20happy%20birthday%20${item.host_user.full_name}%F0%9F%8E%82%0D%0A%0D%0A%0D%0Ayour%20beloved%2C%0D%0A${$UserStore.full_name}`}
            >
              <button class="btn btn-outline-primary">
                send a message</button
              ></a
            >
          </div>
        {/if}
        <hr />
      </div>
      <div class="row">
        <h5>Particpants</h5>
      </div>
      <StackedImages
        stackedImages={[...item.invited_users]}
        bind:itemIndex={clickedParticipantIndex}
      />
      {#if clickedParticipantUser !== undefined && clickedParticipantUser !== null}
        <div class="d-flex flex-column gap-2">
          <div class="d-flex flex-row gap-2">
            <div class="d-flex flex-column gap-1">
              <span class="text-muted">Full Name : </span>
              <span class="text-muted">Team : </span>
              <span class="text-muted">Email :</span>
            </div>
            <div class="d-flex flex-column gap-1">
              <span>{clickedParticipantUser.full_name}</span>
              <span>{clickedParticipantUser.team}</span>
              <span
                ><a
                  href={`mailto:${clickedParticipantUser.email}?subject=Happy%20Birth%20Day%20ahmad&body=Dear%20
                ${clickedParticipantUser.full_name}%2C%0D%0A%0D%0AI%20wish%20you%20a%20happy%20birthday%20${clickedParticipantUser.full_name}
                %F0%9F%8E%82%0D%0A%0D%0A%0D%0Ayour%20beloved%2C%0D%0A${$UserStore.full_name}`}
                  >{clickedParticipantUser.email}
                </a></span
              >
            </div>
          </div>
          {#if Number($UserStore.id) !== Number(item.id)}
            <div class="my-2 right">
              <a
                href={`mailto:${clickedParticipantUser.email}?subject=Happy%20Birth%20Day%20ahmad&body=Dear%20${clickedParticipantUser.full_name}%2C%0D%0A%0D%0AI%20wish%20you%20a%20happy%20birthday%20${clickedParticipantUser.full_name}%F0%9F%8E%82%0D%0A%0D%0A%0D%0Ayour%20beloved%2C%0D%0A${$UserStore.full_name}`}
              >
                <button class="btn btn-outline-primary">
                  send a message</button
                ></a
              >
            </div>
          {/if}
        </div>
      {/if}
    </div>
  </div>
</Modal>

<style>
  .right {
    margin-left: auto;
    margin-right: 0;
  }
</style>
