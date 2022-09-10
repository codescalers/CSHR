<script lang="ts">
  type stackedImageType = {
    image: string;
    alt: string;
    full_name?: string;
    gender?: string;
    team?: string;
  };

  export let stackedImages: stackedImageType[];
  let extra: number = 0;
   //let width: number = 0;
  /* let images: stackedImageType[] = stackedImages;
  let numberOfImages = stackedImages.length;
  $: numberOfImages = Math.ceil(width / 100) + 2;
  $: extra = stackedImages.length - numberOfImages;
  $: images = stackedImages.splice(0, numberOfImages); */
</script>

<div class="d-flex gap-0 px-4" >
  {#each stackedImages as image, index (index)}
    <div
      class="stacked_img"
      style={`background-image:url(${
        image.image?.length === 0
          ? "https://i.imgur.com/9LDfN2H.png"
          : process.env.APP_BASE_API_URL + image.image
      }),url("https://i.imgur.com/9LDfN2H.png");z-index:${
        100 - index
      };border:1.5px solid ${image.gender === "Male" ? "blue" : "pink"}`}
      title={image.full_name + " #" + image.team}
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
    margin-left: -25px;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    padding-left: 1.69rem;
    padding-top: 1.85rem;
    font-size: 1.7rem;
    font-weight: 700;
    letter-spacing: -0.1rem;
    background-color: var(--secondary-color);
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
