<script lang="ts">
  import type { RequestInterface } from "../../types";
  import { fade, scale } from "svelte/transition";
  
  export let request: RequestInterface;
</script>

<tr in:scale out:fade={{ duration: 500 }}>
  <td>{{ request.from_name}}</td>
  <td>{{ request }}</td>
  <td>{{ message }}</td>
  <td>
    <button class={`btn btn-md btn-${type}`} type="button" />
  </td>
</tr>
