<script>
  import DatePicker from "@beyonk/svelte-datepicker/src/components/DatePicker.svelte";

  let selected;
</script>

<!-- <div>
  <DatePicker
    id="siv"
    class="omar"
    range={true}
    on:range-selected={(e) => (selected = e.detail)}
  />
  <div>omar</div>
  <br />
  {JSON.stringify(selected)}
</div> -->




<style>
  #siv {
    font-weight: 900;
    color: "green" !important;
    background-color: "green";
     }
</style>
