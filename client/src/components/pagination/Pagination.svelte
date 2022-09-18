<script lang="ts">
  // page index value
  export let value: number;
  // number of pages
  export let length: number;
  let pages = Array.from({ length: length }, (_, i) => i);

  $: selectedPages = pages.filter(
    (_, index) =>
      index > Number(value) - 2 &&
      index <= Number(value) + 1 &&
      Number(value) <= Number(length) - 1
  );

  $: isPrevDisabled = value === 1;
  $: isNextDisabled = value === length;
  $: isPrevDots = value > 3;
  $: isNextDots = value < length - 2;
</script>

<!-- pagination bootstrap svelte-->
<div class="d-flex  justify-content-end">
  <nav aria-label="Page navigation example">
    <ul class="pagination ">
      <li class="page-item" class:disabled={isPrevDisabled}>
        <a
          class="page-link"
          href="#"
          aria-label="Previous"
          on:click={() => (value -= 1)}
        >
          <span aria-hidden="true">&laquo;</span>
          <span class="sr-only">Previous</span>
        </a>
      </li>
      {#if isPrevDots}
        <li class="page-item">
          <a class="page-link" href="#" on:click={() => (value -= 3)}>...</a>
        </li>
      {/if}
      {#each selectedPages as page (page)}
        <li class="page-item" class:active={value === page + 1}>
          <a class="page-link" href="#" on:click={() => (value = page + 1)}
            >{page + 1}</a
          >
        </li>
      {/each}
      {#if isNextDots}
        <li class="page-item">
          <a class="page-link" href="#" on:click={() => (value += 3)}>...</a>
        </li>
      {/if}
      <li class="page-item" class:disabled={isNextDisabled}>
        <a
          class="page-link"
          href="#"
          aria-label="Next"
          on:click={() => (value += 1)}
        >
          <span aria-hidden="true">&raquo;</span>
          <span class="sr-only">Next</span>
        </a>
      </li>
    </ul>
  </nav>
</div>
