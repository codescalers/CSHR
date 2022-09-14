<script lang="ts">
  type stackedImageType = {
    image: string;
    full_name?: string;
    gender?: string;
    team?: string;
  };

  export let stackedImages: stackedImageType[];
  export let itemIndex: number = 0;

  let extra: number = 0;
  //let width: number = 0;
  /* let images: stackedImageType[] = stackedImages;
  let numberOfImages = stackedImages.length;
  $: numberOfImages = Math.ceil(width / 100) + 2;
  $: extra = stackedImages.length - numberOfImages;
  $: images = stackedImages.splice(0, numberOfImages); */
</script>

<div class="d-flex flex-row gap-0 px-4 unstack flex-wrap align-self-start">
  {#each stackedImages as image, index (index)}
    <div
      class={`stacked_img my-2 ${
        itemIndex === index && stackedImages.length !== 1 ? "activate" : ""
      }`}
      style={`background-image:url(${
        process.env.APP_BASE_API_URL + image.image
      });background-color:${
        image.gender === "Male" ? "#2986cc" : "#FB5858"
      };z-index:${100 - index};border:1.5px solid ${
        image.gender === "Male" ? "var(--secondary-color)" : "pink"
      }`}
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
    overflow: hidden;
    margin-left: -35px;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    padding-left: 1.69rem;
    padding-top: 1.85rem;
    font-size: 1.7rem;
    font-weight: 700;
    letter-spacing: -0.1rem;
    cursor: pointer;
  }
  .activate {
    border: 1px solid rgba(0, 62, 120, 1) !important;
    position: relative;
    bottom: 1.8rem;
    box-shadow: 0px 15px 70px -10px rgba(0, 62, 120, 1.1);
    -webkit-box-shadow: 0px 15px 70px -10px rgba(0, 62, 120, 1.1);
    -moz-box-shadow: 0px 15px 70px -10px rgba(0, 62, 120, 1.1);
  }
  .activate:nth-child(n + 2) {
    margin-left: 5px;
  }
  :global(.stacked_img:nth-child(n + 2):hover) {
    margin-left: 5px;
  }

  .stacked_img .text {
    color: var(--primary-color);
    -webkit-text-stroke: 0.9px var(--secondary-color); /* width and color */
  }
  .stacked_img .extra {
    color: grey;
    -webkit-text-stroke: 0.9px white; /* width and color */
  }
</style>
