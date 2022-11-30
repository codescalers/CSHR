<script lang="ts">
  import type { stackedImageType } from "../../utils/types";

  export let stackedImages: stackedImageType[];
  export let itemIndex: number = 0;

  let extra: number = 0;
</script>

<div class="d-flex flex-row gap-0 px-4 unstack flex-wrap align-self-start">
  {#each stackedImages as image, index (index)}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    {#if image.image.includes("profile_image")}
      {#if image.image[0] == "/"}
        <!-- svelte-ignore a11y-missing-attribute -->
        <img
          class={`profile-image stacked_img my-2 ${
            itemIndex === index && stackedImages.length !== 1 ? "activate" : ""
          }`}
          src={window.configs.SERVER_API_URL?.slice(0, -1) + image.image}
          on:click={() => (itemIndex = index)}
        />
      {:else}
        <div
          class={`stacked_img my-2 ${
            itemIndex === index && stackedImages.length !== 1 ? "activate" : ""
          }`}
          style="background-image:url({window.configs.SERVER_API_URL +
            image.image});z-index:${100 - index};border:1.5px solid"
          data-bs-toggle="tooltip"
          title={image.full_name + " #" + image.team}
          on:click={() => (itemIndex = index)}
        />
      {/if}
    {:else}
      <div
        class={`stacked_img my-2 ${
          itemIndex === index && stackedImages.length !== 1 ? "activate" : ""
        }`}
        style="background-color:{image.image};z-index:${100 -
          index};color: #fff"
        data-bs-toggle="tooltip"
        title={image.full_name + " #" + image.team}
        on:click={() => (itemIndex = index)}
      >
        {#if image.full_name}
          <span class="text">
            {image.full_name?.split(" ")[0].charAt(0).toUpperCase() +
              "" +
              (image.full_name?.split(" ")[1].charAt(0) + "").toUpperCase()}
          </span>
        {/if}
      </div>
    {/if}
  {/each}
  {#if extra > 0}
    <div
      class="stacked_img"
      style="background-image:url('https://i.imgur.com/9LDfN2H.png')"
    >
      <span class="extra">{"+" + extra}</span>
    </div>
  {/if}
</div>

<style>
  :global(.stacked_img) {
    width: 4.7rem;
    height: 4.7rem;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1.7rem;
    font-weight: 700;
    cursor: pointer;
  }
  .profile-image {
    width: 4.7rem;
    height: 4.7rem;
    border-radius: 50%;
  }
  .activate {
    position: relative;
    bottom: 1.8rem;
  }
  .activate:nth-child(n + 2) {
    margin-left: 5px;
  }
  :global(.stacked_img:nth-child(n + 2):hover) {
    margin-left: 5px;
  }

  .stacked_img .text {
    color: #fff;
    -webkit-text-stroke: 0.9px var(--secondary-color); /* width and color */
  }
  .stacked_img .extra {
    color: grey;
    -webkit-text-stroke: 0.9px white; /* width and color */
  }
</style>
