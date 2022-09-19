<script lang="ts">
  import { onMount } from "svelte";
  import Table from "../table/Table.svelte";
  onMount(async () => {});
  let pageIndex: number = 0;
  let length: number = 10;
  let headers = [
    "Name",
    "Email",
    "Phone",
    "Address",
    "Company",
    "Website",
    "Actions",
  ];
</script>

<div>
  <Table bind:pageIndex bind:length bind:headers>
    <div slot="table-body" />
  </Table>
</div>
