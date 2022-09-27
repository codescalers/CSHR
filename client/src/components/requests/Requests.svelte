<script lang="ts">
  import type { RequestInterface } from '../../types';
  import Request from './Request.svelte';
  let requests: RequestInterface[];
</script>

<div class="container">
  <div class="table-responsive">
    <table class="table table-striped table-hover table-sm">
      <thead>
        <tr>
          <th>From</th>
          <th>type</th>
          <th>message</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {#each requests as request (request.id)}
          <Request {request} />
        {/each}
      </tbody>
    </table>
  </div>
</div>
