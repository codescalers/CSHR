<script lang="ts">
  import type { eventItemType, userType } from '../../services/axios/home/types'
  import { UserStore } from '../../stores'
  import Modal from '../modal/Modal.svelte'
  import StackedImages from '../image/StackedImages.svelte'

  export let item: eventItemType
  let itemIndex: number = 0
  let clickedUser: userType
  $: clickedUser = item.people[itemIndex]
</script>

<Modal
  bind:id={item.id}
  isDelete={false}
  isDone={false}
  doneText={''}
  on:onDelete
  on:onDone
  deleteText={''}
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
        <div>{''}</div>
        <div class="d-flex flex-column justify-content-between gap-2">
          <div class="d-flex flex-row justify-content-between gap-2">
            <span>
              {`${item.from_date.getDate()}/${item.from_date.getMonth()}.${item.from_date.getFullYear()}`}
            </span>
            <span>
              {`${item.end_date.getDate()}/${item.end_date.getMonth()}.${item.end_date.getFullYear()}`}
            </span>
          </div>
          <div>{item.from_time} - {item.end_time}</div>
        </div>
      </div>
    </h6>
    <div class="container d-flex flex-column gap-5 px-5 my-5">
      <StackedImages stackedImages={[...item.people]} bind:itemIndex />
      {#if itemIndex !== null && clickedUser !== undefined && clickedUser !== null}
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
        </div>
      {/if}
    </div>
  </div>
</Modal>
