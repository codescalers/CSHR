<script lang="ts">
  import { onMount } from "svelte";
  export let src: string,
    alt: string,
    className: string = "";

  let loaded = false;
  let failed = false;
  let loading = false;

  onMount(() => {
    const img = new Image();
    img.src = src;
    loading = true;

    img.onload = () => {
      loading = false;
      loaded = true;
    };
    img.onerror = () => {
      loading = false;
      failed = true;
    };
  });
</script>

{#if loaded}
  <img {src} {alt} class={className} />
{:else if failed}
  <img
    src="https://icon-library.com/images/not-found-icon/not-found-icon-20.jpg"
    alt="Not Found"
    class={className}
  />
{:else if loading}
  <img
    class={"loader " + className}
    src="https://c.tenor.com/On7kvXhzml4AAAAi/loading-gif.gif"
    alt="Loading..."
  />
{/if}

<style>
  .loader {
    width: 25px;
    height: 25px;
    text-align: center;
    transform: translate(0, 100px);
  }
</style>
