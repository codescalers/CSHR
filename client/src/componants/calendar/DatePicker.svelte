<script context="module">
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
</script>

<script>
  export let days = "Su|Mo|Tu|We|Th|Fr|Sa".split("|");
  export let months = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec".split(
    "|"
  );
  export let onlyStart;
  export let start = 0; // first day of the week (0 = Sunday, 1 = Monday)
  export let offset = 0; // offset in months from currently selected date

  export let startDate = iso(new Date());
  export let endDate = iso(new Date());

  $: acceptDate(startDate, endDate);

  function acceptDate(value, value2) {
    const newDate = new Date(value);
    const newDate2 = new Date(value2);

    if (!isNaN(newDate)) {
      startDate = iso(newDate);
    }
    if (!isNaN(newDate2)) {
      endDate = iso(newDate2);
    }
  }

  function go(direction) {
    offset = offset + direction;
  }

  function selectDate(newValue, flag) {
    if (onlyStart) {
      startDate = newValue;
      endDate = newValue;
    } else {
      if (flag) {
        startDate = newValue;
      } else {
        if (newValue < startDate) {
          endDate = startDate;
          startDate = newValue;
        } else {
          endDate = newValue;
        }
      }
    }

    offset = 0;
  }

  $: viewDate = viewDateFrom(startDate, offset);

  $: month = months[viewDate.getMonth()];

  $: year = viewDate.getFullYear();

  $: weeks = weeksFrom(viewDate, startDate, endDate, start);

  function viewDateFrom(date, offset) {
    var viewDate = new Date(date);
    viewDate.setMonth(viewDate.getMonth() + offset);
    return viewDate;
  }

  function weeksFrom(viewDate, startDay, endDay, start) {
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
          startDay === value || (endDay === value && !onlyStart)
            ? "selected"
            : "",
          startDay < value && endDay > value && !onlyStart
            ? "rangeSelected"
            : "",

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

<div id="highlight" class="d-flex flex-row">
  <!-- svelte-ignore a11y-mouse-events-have-key-events -->
  <div class="arrows"><button on:mouseover={() => go(-1)}>&lt;</button></div>

  <table class="table table-striped table-hover">
    <tr>
      <td><button class="go-btn" on:click={() => go(-1)}>&lt;</button></td>
      <td colspan="5" class="table-header">{month} {year}</td>
      <td><button class="go-btn" on:click={() => go(+1)}>&gt;</button></td>
    </tr>
    <thead>
      <tr>
        {#each days as day (day)}
          <th scope="col">{day}</th>
        {/each}
      </tr>
    </thead>
    {#each weeks as week (week)}
      <tr>
        {#each week as day, i (i)}
          <td
            class="day {day.class} py-sm-3 py-xlg-0 px-sm-0 px-xlg-5"
            data-date={day.value}
            on:mousedown={function (e) {
              const arrows = document.querySelectorAll(".arrows");
              arrows.forEach((arrow) => {
                arrow.classList.add("arrowsVisible");
              });
              selectDate(this.getAttribute("data-date"), true);
            }}
            on:mouseup={function (e) {
              const arrows = document.querySelectorAll(".arrows");
              arrows.forEach((arrow) => {
                arrow.classList.remove("arrowsVisible");
              });
              selectDate(this.getAttribute("data-date"), false);
            }}>{(day.date + "").length === 1 ? day.date + " " : day.date}</td
          >
        {/each}
      </tr>
    {/each}
  </table>
  <!-- svelte-ignore a11y-mouse-events-have-key-events -->
  <div class="arrows"><button on:mouseover={() => go(+1)}>&gt;</button></div>
</div>

<style>
  .arrows {
    font-size: 1.5rem;
    cursor: pointer;
    background-color: rgb(43 81 95);
    color: rgb(255 255 255);
    border-radius: 50%;
    font-weight: 900;
    margin: auto;
    overflow: hidden;
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    visibility: hidden;
  }
  .arrowsVisible {
    visibility: visible;
  }
  .arrows button {
    background-color: transparent;
    border: none;
    color: rgb(255 255 255);
  }
  .rangeSelected {
    background-color: rgb(43 81 95 / 24%);
    border-radius: 50%;
  }
  .table-header {
    font-size: 1.2rem;
    text-align: center;
    color: #273142;
  }
  table {
    color: #9cb2cd;
    padding: 0;
    margin: 0;
    width: 90%;
  }

  td.past,
  td.future {
    opacity: 0.3;
    cursor: not-allowed;
  }
  .go-btn {
    cursor: pointer;
    color: rgb(255 255 255);
    border-radius: 5px;
    font-size: 1rem;
    cursor: pointer;
    background-color: rgb(43 81 95);
    font-weight: 600;
    border: rgb(215 227 241) 1px solid;
    padding: 0.4rem 0.7rem;
    margin-top: 8px;
  }
  .day {
    cursor: pointer;
    text-align: center;
    width: 60px;
  }

  .day.selected,
  .day.selected:hover,
  .day.selected::selection,
  .day.selected:hover::selection {
    width: 60px;
    text-align: center;
    background-color: #2b515f;
    border-radius: 50%;
    color: #fff;
  }

  .day:hover,
  .day:hover::selection {
    width: 60px;
    text-align: center;
    background-color: #6ea3b6;
    color: #fff;
    border-radius: 50%;
  }

  .day::selection {
    background-color: #eff6ff;
  }
  ::selection {
    background-color: #fff;
  }
</style>
