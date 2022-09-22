<script lang="ts">
  let searchInput: HTMLInputElement;

  async function searchFunction() {
    const word = searchInput.value;
    if (word.length > 0) {
    } else {
    }
  }
</script>

<div class="input-group">
  <input
    bind:this={searchInput}
    type="search"
    class="form-control rounded input"
    placeholder="Search"
    aria-label="Search"
    aria-describedby="search-addon"
  />
  <button
    type="button"
    class="btn btn-outline-primary"
    on:click={searchFunction}
  >
    Search
  </button>
</div>
