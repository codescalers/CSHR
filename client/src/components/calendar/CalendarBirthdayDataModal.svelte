<script lang="ts">
  //  import { ConfettiExplosion } from "svelte-confetti-explosion";
  export let item: birthDateItemType;

  onMount(() => {
    /*  const confetti = new ConfettiExplosion({
      props: {
        colors: ["#2986cc", "#FB5858"],
        duration: 5000,
      },
    });
    {
      confetti.start();
    } */
  });
  import type {
    birthDateItemType,
    userType,
  } from '../../services/axios/home/types';
  import { UserStore } from '../../stores';
  import Modal from '../modal/Modal.svelte';
  import StackedImages from '../image/StackedImages.svelte';
  import { onMount } from 'svelte';

  let itemIndex: number = 0;
  let clickedUser: userType;
  $: clickedUser = item.users[itemIndex];

  let header =
    item.users.length > 1
      ? 'Wish them a Happy Birthday !'
      : `Wish ${item.users[0].gender === 'Male' ? 'him' : 'her'} a BirthDay ! `;
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
  <div slot="body" class="bg-confetti-animated">
    <div class="container d-flex flex-column gap-5 px-5 my-5">
      <h3 class="mx-auto text-muted">{header}</h3>
      <StackedImages stackedImages={[...item.users]} bind:itemIndex />
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
  </div></Modal
>

<style>
  .right {
    margin-left: auto;
    margin-right: 0;
  }

  :global(:root) {
    --y: -500px;
  }
  .bg-confetti-animated {
    background-repeat: repeat-x;
    background-position: top -10px center;
    background-image: url("data:image/svg+xml,%3Csvg width='600' height='90' viewBox='0 0 600 90' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Crect x='42' y='-10' width='6' height='10'/%3E%3Crect x='84' y='-10' width='6' height='10'/%3E%3Crect x='126' y='-13' width='5' height='13'/%3E%3Crect x='168' y='-13' width='5' height='13'/%3E%3Crect x='210' y='-10' width='6' height='10'/%3E%3Crect x='252' y='-13' width='5' height='13'/%3E%3Crect x='294' y='-10' width='6' height='10'/%3E%3Crect x='336' y='-13' width='5' height='13'/%3E%3Crect x='378' y='-13' width='5' height='13'/%3E%3Crect x='420' y='-10' width='6' height='10'/%3E%3Crect x='462' y='-10' width='6' height='10'/%3E%3Crect x='504' y='-13' width='5' height='13'/%3E%3Crect x='546' y='-10' width='6' height='10'/%3E%3Cstyle type='text/css'%3E rect %7B opacity: 0; %7D rect:nth-child(1) %7B transform-origin: 45px 5px; transform: rotate(-145deg); animation: blast 700ms infinite ease-out; animation-delay: 88ms; animation-duration: 631ms; %7D rect:nth-child(2) %7B transform-origin: 87px 5px; transform: rotate(164deg); animation: blast 700ms infinite ease-out; animation-delay: 131ms; animation-duration: 442ms; %7D rect:nth-child(3) %7B transform-origin: 128px 6px; transform: rotate(4deg); animation: blast 700ms infinite ease-out; animation-delay: 92ms; animation-duration: 662ms; %7D rect:nth-child(4) %7B transform-origin: 170px 6px; transform: rotate(-175deg); animation: blast 700ms infinite ease-out; animation-delay: 17ms; animation-duration: 593ms; %7D rect:nth-child(5) %7B transform-origin: 213px 5px; transform: rotate(-97deg); animation: blast 700ms infinite ease-out; animation-delay: 122ms; animation-duration: 476ms; %7D rect:nth-child(6) %7B transform-origin: 255px 6px; transform: rotate(57deg); animation: blast 700ms infinite ease-out; animation-delay: 271ms; animation-duration: 381ms; %7D rect:nth-child(7) %7B transform-origin: 297px 5px; transform: rotate(-46deg); animation: blast 700ms infinite ease-out; animation-delay: 131ms; animation-duration: 619ms; %7D rect:nth-child(8) %7B transform-origin: 338px 6px; transform: rotate(-65deg); animation: blast 700ms infinite ease-out; animation-delay: 85ms; animation-duration: 668ms; %7D rect:nth-child(9) %7B transform-origin: 380px 6px; transform: rotate(13deg); animation: blast 700ms infinite ease-out; animation-delay: 128ms; animation-duration: 377ms; %7D rect:nth-child(10) %7B transform-origin: 423px 5px; transform: rotate(176deg); animation: blast 700ms infinite ease-out; animation-delay: 311ms; animation-duration: 508ms; %7D rect:nth-child(11) %7B transform-origin: 465px 5px; transform: rotate(108deg); animation: blast 700ms infinite ease-out; animation-delay: 108ms; animation-duration: 595ms; %7D rect:nth-child(12) %7B transform-origin: 506px 6px; transform: rotate(62deg); animation: blast 700ms infinite ease-out; animation-delay: 105ms; animation-duration: 375ms; %7D rect:nth-child(13) %7B transform-origin: 549px 5px; transform: rotate(16deg); animation: blast 700ms infinite ease-out; animation-delay: 149ms; animation-duration: 491ms; %7D rect:nth-child(odd) %7B fill: %2365BB5C; %7D rect:nth-child(even) %7B z-index: 1; fill: %2333AAFF; %7D rect:nth-child(4n) %7B animation-duration: 1400ms; fill: %23F23B14; %7D rect:nth-child(3n) %7B animation-duration: 1750ms; animation-delay: 700ms; %7D rect:nth-child(4n-7) %7B fill: %232A2F6A; %7D rect:nth-child(6n) %7B fill: %23FBBA23; %7D @keyframes blast %7B from %7B opacity: 0; %7D 20%25 %7B opacity: 1; %7D to %7B transform: translateY(90px); %7D %7D %3C/style%3E%3C/svg%3E%0A");
  }
</style>
