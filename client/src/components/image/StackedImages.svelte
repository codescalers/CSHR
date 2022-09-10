<script lang="ts">
  import Image from "./Image.svelte";
  type stackedImageType = { src: string; alt: string };
  export let stackedImages: stackedImageType[] = [];
</script>

<div class="d-flex gap-0 px-4">
  {#each stackedImages as image}
    <Image src={image.src} alt="user-avatar" className="stacked_img" />
  {/each}
  <Image
    src="https://i.imgur.com/hczKIze.jpg"
    alt="personal-image"
    className={"stacked_img"}
  />
  <Image
    src="https://i.imgur.com/hczKIze.jpg"
    alt="personal-image"
    className={"stacked_img"}
  />
  <Image
    src="https://i.imgur.com/hczKIze.jpg"
    alt="personal-image"
    className={"stacked_img"}
  />
</div>

<style>
  :global(.stacked_img) {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    overflow: hidden;
    margin-left: -10px;
  }
</style>
