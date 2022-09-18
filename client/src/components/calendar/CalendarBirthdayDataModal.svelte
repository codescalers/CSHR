<script lang="ts">
  import type {
    birthDateItemType,
    userType,
  } from "../../services/axios/home/types";
  import { UserStore } from "../../stores";
  import Modal from "../modal/Modal.svelte";
  import StackedImages from "../image/StackedImages.svelte";

  export let item: birthDateItemType;
  let itemIndex: number = 0;
  let clickedUser: userType;
  $: clickedUser = item.users[itemIndex];

  let header =
    item.users.length > 1
      ? "Wish them a Happy Birthday !"
      : `Wish ${item.users[0].gender === "Male" ? "him" : "her"} a BirthDay ! `;
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
  <header slot="header">
    <h6 class="modal-title" id="exampleModalLongTitle">
      {item.title.toUpperCase()}
    </h6>
  </header>
  <div slot="body">
    <div class="container d-flex flex-column gap-5 px-5 my-5">
      <h3 class="mx-auto text-muted">{header}</h3>
      <StackedImages stackedImages={[...item.users]} bind:itemIndex />
      {#if itemIndex !== null && clickedUser!==undefined && clickedUser!==null}
        <div class="d-flex flex-column gap-2">
          <div class="row" style="" />
          <div class="d-flex flex-row gap-2">
            <div class="d-flex flex-column gap-1">
              <span class="text-muted">Full Name : </span>
              <span class="text-muted">Team : </span>
              <span class="text-muted">Email :</span>
            </div>
            <div class="d-flex flex-column gap-1">
              <span>{clickedUser.full_name}</span>
              <span>{clickedUser.team}</span>
              <span
                ><a
                  href={`mailto:${clickedUser.email}?subject=Happy%20Birth%20Day%20ahmad&body=Dear%20${clickedUser.full_name}%2C%0D%0A%0D%0AI%20wish%20you%20a%20happy%20birthday%20${clickedUser.full_name}%F0%9F%8E%82%0D%0A%0D%0A%0D%0Ayour%20beloved%2C%0D%0A${$UserStore.full_name}`}
                  >{clickedUser.email}
                </a></span
              >
            </div>
          </div>
          {#if Number($UserStore.id) !== Number(item.id)}
            <div class="my-2 right">
              <a
                href={`mailto:${clickedUser.email}?subject=Happy%20Birth%20Day%20ahmad&body=Dear%20${clickedUser.full_name}%2C%0D%0A%0D%0AI%20wish%20you%20a%20happy%20birthday%20${clickedUser.full_name}%F0%9F%8E%82%0D%0A%0D%0A%0D%0Ayour%20beloved%2C%0D%0A${$UserStore.full_name}`}
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
