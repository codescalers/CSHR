<script>
  import DatePicker from "./Datepicker.svelte";
  let onlyStart = false;
  let startDate = "2022-03-01";
  let endDate = "2022-03-03";

  const locale = {
    en: {
      days: "Su|Mo|Tu|We|Th|Fr|Sa".split("|"),
      months: "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec".split("|"),
      start: 0,
    },
    da: {
      days: "Sø|Ma|Ti|On|To|Fr|Lø".split("|"),
      months: "Jan|Feb|Mar|Apr|Maj|Jun|Jul|Aug|Sep|Okt|Nov|Dec".split("|"),
      start: 1,
    },
  };

  let culture = "en";
</script>

<div class="container table-primary table-responsive">
  <DatePicker bind:startDate bind:endDate bind:onlyStart {...locale[culture]} />
  <form>
    <div class="form-group row">
      <label for="colFormLabel" class="col-sm-3 col-form-label py-3"
        >Start Date</label
      >
      <div class="col-sm-6">
        <input
          type="text"
          class="form-control"
          id="colFormLabel"
          bind:value={startDate}
        />
      </div>
    </div>
    {#if !onlyStart}
      <div class="form-group row">
        <label for="colFormLabel" class="col-sm-3 col-form-label py-3"
          >End Date</label
        >
        <div class="col-sm-6">
          <input
            bind:value={endDate}
            type="text"
            class="form-control"
            id="colFormLabel"
            color="#EDF2F9"
          />
        </div>
      </div>
    {/if}

    <button class="btn btn-primary">Submit</button>
  </form>
</div>

<style>
  input[type="text"] {
    margin-top: 0.3cm;
    background-color: #edf2f9;
  }
  button {
    margin-top: 0.5cm;
    font-size: 16px;
    color: #2b515f;
    background-color: #eff6ff;
    width: 10cm;
  }
</style>
