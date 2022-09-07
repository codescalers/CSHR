<script lang="ts">
  import DatePicker from "./Datepicker.svelte";
  export let error_message = "";
  export let onlyStart = false;
  export let isLoading = false;
  let startDate = "2022-03-01";
  let endDate = "2022-03-03";

  const locale: {
    en: {
      days: string[];
      months: string[];
      start: number;
    };
  } = {
    en: {
      days: "Su|Mo|Tu|We|Th|Fr|Sa".split("|"),
      months: "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec".split("|"),
      start: 0,
    },
  };
  function validateDate(date: string, error_name: string) {
    let check = Date.parse(date);
    if (!check) {
      //it is not a date with format YYYY-MM-DD
      //alert("Date is unvalid");
      error_message = `${error_name} format is invalid message`;
    } else {
      //alert("date");
      error_message = "";
    }
    //it is a date with format YYYY-MM-DD
  }
  $: validateDate(startDate, "Start Date");
  $: validateDate(endDate, "End Date");
</script>

<div class="container table-primary table-responsive">
  <fieldset
    id="isloading"
    disabled={isLoading}
    style={` opacity: ${isLoading ? "0.1" : "1"}`}
  >
    {#if !error_message}
      <div>
        <DatePicker
          bind:startDate
          bind:endDate
          bind:onlyStart
          {...locale["en"]}
        />
      </div>
    {:else}
      <div class="alert alert-danger" role="alert">
        {error_message}
      </div>
    {/if}

    <div class="mx-5">
      <slot name="toggler" />

      <div class="my-4 px-3">
        <div class="form-group row pl-5">
          <label for="colFormLabel" class="col-sm-4 col-form-label py-3"
            >{!onlyStart ? "Start " : ""}Date</label
          >
          <div class="col-sm-8">
            <input
              type="text"
              bind:value={startDate}
              class={`form-control ${
                error_message.charAt(0) === "S"
                  ? "is-invalid error-border text-danger"
                  : ""
              } `}
              color="#EDF2F9"
              id="validationServer01"
              aria-describedby="validationServer01Feedback"
              required
            />

            <div id="validationServer01Feedback" class="invalid-feedback">
              Please provide a valid Start Date with this Format YYYY-MM-DD.
            </div>
          </div>
        </div>

        {#if !onlyStart}
          <div class="form-group row">
            <label for="colFormLabel" class="col-sm-4 col-form-label py-3"
              >End Date</label
            >
            <div class="col-sm-8">
              <input
                bind:value={endDate}
                type="text"
                class={`form-control ${
                  error_message.charAt(0) === "E"
                    ? "is-invalid error-border text-danger"
                    : ""
                } `}
                color="#EDF2F9"
                id="validationServer02"
                aria-describedby="validationServer02Feedback"
                required
              />
              <div id="validationServer02Feedback" class="invalid-feedback">
                Please provide a valid End Date with this Format YYYY-MM-DD.
              </div>
            </div>
          </div>
        {/if}
        <slot name="form" />
      </div>
    </div>
  </fieldset>
</div>

<style>
  input[type="text"] {
    margin-top: 0.4cm;
    background-color: #edf2f9;
  }
  .put-left {
    margin-left: -1.5cm;
  }
</style>
