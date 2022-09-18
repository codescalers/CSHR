<script lang="ts">
  import type { vacationItemType } from "../../services/axios/home/types";
  import { UserStore } from "../../stores";
  import Modal from "../modal/Modal.svelte";

  export let item: vacationItemType;
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
    <h6 class="modal-title" id="exampleModalLongTitle">
      <div class="d-flex flex-row justify-content-between gap-2">
        <div>{""}</div>
        <div class="d-flex flex-row justify-content-between gap-2">
          <span>
            {`${item.from_date}`}
          </span>
          <span>
            {`${item.end_date}`}
          </span>
        </div>
      </div>
    </h6>
    <div class="container d-flex flex-column gap-5 px-5 my-5">
      <div class="d-flex flex-column gap-2">
        <div class="row" style="" />
        <div class="d-flex flex-row gap-2">
          <div class="d-flex flex-column gap-1">
            <span class="text-muted">Full Name : </span>
            <span class="text-muted">Team : </span>
            <span class="text-muted">Email :</span>
          </div>
          <div class="d-flex flex-column gap-1">
            <span>{item.applying_user.full_name}</span>
            <span>{item.applying_user.team}</span>
            <span
              ><a
                href={`mailto:${item.applying_user.email}?subject=Happy%20Birth%20Day%20ahmad&body=Dear%20${item.applying_user.full_name}%2C%0D%0A%0D%0AI%20wish%20you%20a%20happy%20birthday%20${item.applying_user.full_name}%F0%9F%8E%82%0D%0A%0D%0A%0D%0Ayour%20beloved%2C%0D%0A${$UserStore.full_name}`}
                >{item.applying_user.email}
              </a></span
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</Modal>
