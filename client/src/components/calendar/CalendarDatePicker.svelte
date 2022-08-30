<script>
  import DatePicker from "./Datepicker.svelte";

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
  <input type="text" bind:value={startDate} />
  <DatePicker bind:value={startDate} {...locale[culture]} />

</div>
