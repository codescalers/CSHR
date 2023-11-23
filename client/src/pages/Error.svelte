<script lang="ts">
  export let error: number;
</script>

{#if error}
  <div class="error">
    <div class="error-text">
      <img src="https://icon-library.com/images/not-found-icon/not-found-icon-20.jpg" alt="Not Found" />
      <h1>Page Not Found</h1>
      <p>Sorry, but the page you were trying to view does not exist.</p>
    </div>
  </div>

  <style>
    * {
      line-height: 1.2;
      margin: 0;
    }

    .error {
      color: #888;
      display: table;
      font-family: sans-serif;
      height: 100%;
      text-align: center;
      width: 100%;
    }
    .error-text {
      display: table-cell;
      vertical-align: middle;
      margin: 2em auto;
    }
    h1 {
      color: #555;
      font-size: 2em;
      font-weight: 400;
    }
    p {
      margin: 0 auto;
      width: 280px;
    }
    @media only screen and (max-width: 280px) {
      .error-text,
      p {
        width: 95%;
      }
      h1 {
        font-size: 1.5em;
        margin: 0 0 0.3em;
      }
    }
  </style>
{/if}
