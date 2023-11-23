<script lang="ts">
  import "flatpickr/dist/flatpickr.css";
  import "flatpickr/dist/themes/light.css";

  import Flatpickr from "svelte-flatpickr";

  export let date: any = null;

  const flatpickrOptions = {
    mode: "multiple",
    element: "#my-picker",
  };
</script>

<Flatpickr options={flatpickrOptions} bind:value={date} element="#my-picker">
  <div class="flatpickr form-outline mb-4" id="my-picker">
    <div class="form-group row">
      <div class="col-4">
        <label class="col-sm-4 col-form-label py-3" for="datePickerInput">Public holidays</label>
      </div>
      <div class="col-sm-8">
        <input class="form-control" id="datePickerInput" type="text" placeholder="Select Date.." data-input />
      </div>
    </div>
  </div>
</Flatpickr>

<style>
  input {
    margin-top: 0.3cm !important;
    background-color: var(--secondary-color) !important;
  }
  .form-control {
    display: block;
    width: 100%;
    padding: 0.375rem 0.75rem;
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.5;
    color: rgb(33 37 41);
    background-color: rgb(255 255 255);
    background-clip: padding-box;
    border: 1px solid rgb(206 212 218);
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
    border-radius: 0.375rem;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  }
</style>
