<script lang="ts">
  import { onMount } from "svelte";
  import { AllUsersStore } from "../../stores";

  export let option: any;
  let image: string;
  onMount(() => {
    image = $AllUsersStore.find((user: any) => user.full_name === option).image;
  });

  let hidden = false;
  // default back to visible every time src changes to see if the image loads successfully
  $: image, (hidden = false);
</script>

<span class="option">
  <img
    src={image}
    alt={"user avatar"}
    {hidden}
    on:error={() => (hidden = true)}
  /><span>{option}</span>
</span>

<style>
  img {
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    object-fit: cover;
  }
  .option {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  span span {
    font-size: 1rem;
    font-weight: 400;
    text-align: right;
  }
</style>
