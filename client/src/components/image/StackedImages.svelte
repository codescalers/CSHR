<script lang="ts">
  type stackedImageType = {
    src: string;
    alt: string;
    userName?: string;
    gender?: string;
  };

  export let stackedImages: stackedImageType[] = [];
  export let limit: boolean = false;
  export let extra: number = 1;
</script>

<div class="d-flex gap-0 px-4">
  {#each stackedImages as image, index (index)}
    <div
      class="stacked_img"
      style={`background-image:url(${image.src});z-index:${
        100 - index
      };border:1px solid ${image.gender === "male" ? "blue" : "pink"}`}
    >
      {#if image.userName}
        <span>
          {image.userName?.split(" ")[0].charAt(0).toUpperCase() +
            "" +
            (image.userName?.split(" ")[1].charAt(0) + "").toUpperCase()}
        </span>
      {/if}
    </div>
  {/each}
  {#if limit}
    <div
      class="stacked_img"
      style="background-image:url('https://i.imgur.com/9LDfN2H.png')"
    >
      <span class="extra">{"+" + extra}</span>
    </div>
  {/if}
</div>

<style>
  .stacked_img {
    width: 4.7rem;
    height: 4.7rem;
    border-radius: 50%;
    overflow: hidden;
    margin-left: -25px;
    text-align: left;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    padding-left: 0.5rem;
    padding-top: 1.85rem;
    font-size: 1.7rem;
    font-weight: 700;
    letter-spacing: 0rem;
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
