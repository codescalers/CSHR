<script>
  export function iso(date) {
    const pad = (n) => (n < 10 ? "0" + n : n);
    return (
      date.getFullYear() +
      "-" +
      pad(date.getMonth() + 1) +
      "-" +
      pad(date.getDate())
    );
  }

  export let value = iso(new Date());
  export let days = "Su|Mo|Tu|We|Th|Fr|Sa".split("|");
  export let months = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec".split(
    "|"
  );
  export let start = 0; // first day of the week (0 = Sunday, 1 = Monday)
  export let offset = 0; // offset in months from currently selected date

  let date = iso(new Date());

  $: acceptDate(value);

  function acceptDate(value) {
    const newDate = new Date(value);

    if (!isNaN(newDate)) {
      date = iso(newDate);
    }
  }

  function go(direction) {
    offset = offset + direction;
  }

  function selectDate(newValue) {
    date = newValue;
    value = newValue;
    offset = 0;
  }

  $: viewDate = viewDateFrom(date, offset);

  $: month = months[viewDate.getMonth()];

  $: year = viewDate.getFullYear();

  $: weeks = weeksFrom(viewDate, date, start);

  function viewDateFrom(date, offset) {
    var viewDate = new Date(date);
    viewDate.setMonth(viewDate.getMonth() + offset);
    return viewDate;
  }

  function weeksFrom(viewDate, date, start) {
    var first = new Date(viewDate.getTime());
    first.setDate(1);
    first.setDate(first.getDate() + ((start - first.getDay() - 7) % 7));

    var last = new Date(viewDate.getTime());
    last.setDate(
      new Date(viewDate.getFullYear(), viewDate.getMonth() + 1, 0).getDate()
    );
    last.setDate(last.getDate() + ((start - last.getDay() + 6) % 7));

    var d = new Date(first.getTime()),
      M = viewDate.getMonth(),
      Y = viewDate.getFullYear(),
      week = [],
      weeks = [week];

    while (d.getTime() <= last.getTime()) {
      var dd = d.getDate(),
        mm = d.getMonth(),
        yy = d.getFullYear(),
        value = iso(d);

      week.push({
        date: dd,
        value,
        class: [
          date === value ? "selected" : "",
          mm == M ? "" : (mm > M ? yy >= Y : yy > Y) ? "future" : "past",
        ].join(" "),
      });

      d = new Date(d.getFullYear(), d.getMonth(), d.getDate() + 1);

      if (d.getDay() === start) {
        week = [];
        weeks.push(week);
      }
    }

    return weeks;
  }
</script>

<table class="table table-striped table-hover ">
  <tr>
    <td><button class="go-btn" on:click={() => go(-1)}>&lt;</button></td>
    <td colspan="5" class="table-header">{month} {year}</td>
    <td><button class="go-btn" on:click={() => go(+1)}>&gt;</button></td>
  </tr>
  <thead>
    <tr>
      {#each days as day}
        <th scope="col">{day}</th>
      {/each}
    </tr>
  </thead>
  {#each weeks as week}
    <tr>
      {#each week as day}
        <td class="day {day.class}" on:click={() => selectDate(day.value)}
          >{day.date}</td
        >
      {/each}
    </tr>
  {/each}
</table>

<style>
  .table-header {
    font-size: 1.4rem;
    text-align: center;
    color: #273142;
  }
  table {
    color: #9cb2cd;
    padding: 0;
    margin: 0;
  }

  td.past,
  td.future {
    opacity: 0.5;
  }
  .go-btn {
    cursor: pointer;
    color: #9cb2cd;
    background-color: #fff;
    border: 1px solid #9cb2cd;
    text-align: center;
    border-radius: 20%;
    font-weight: 600;
    width: 90%;
    margin: 0.3rem;
    font-size: 1rem;
  }
  .go-btn:hover {
    background-color: #2b515f;
    cursor: pointer;
    color: #fff;
    font-weight: 600;
    border: #d7e3f1 1px solid;
    padding: 0.3rem 0.5rem;
  }
  .day {
    cursor: pointer;
    text-align: center;
    padding: 0.5rem 0rem;
  }
  .day.selected {
    background-color: #2b515f;
    color: #fff;
    border-radius: 100%;
    padding: 0.5rem 0rem;
    aspect-ratio: 1;
  }

  .day:hover {
    background: gray;
    color: white;
  }
  td.selected {
    color: #ffffff;
    font-weight: bold;
    background-color: #006dcc;
    border-color: #002a80;
  }
</style>
