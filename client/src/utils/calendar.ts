import homePage from "../apis/home/home";
import type { calendarItemsType } from "./types";

export const dayNames = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

export const monthNames = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December"
];

export const removeUnUsedModal = () => {
  const modalBackdrop = document.getElementsByClassName("modal-backdrop show");
  if (modalBackdrop.length && modalBackdrop[0].parentNode) {
    modalBackdrop[0].parentNode.removeChild(modalBackdrop[0]);
  }
};

export async function calendarData(
  isLoading: boolean,
  month: number,
  year: number,
  items: calendarItemsType[]
): Promise<calendarItemsType[]> {
  removeUnUsedModal();
  isLoading = true;
  try {
    const calendarItems = await homePage.eventCalendarAPI(month + 1, year);
    items = calendarItems.results;
  } catch (error: any) {
    console.log(error);
  }
  isLoading = false;
  return items;
}

export function findRowCol(dt: Date, days: any[]) {
  for (let i = 0; i < days.length; i++) {
    const d = days[i].date;
    if (
      d.getFullYear() === dt.getFullYear() &&
      d.getMonth() === dt.getMonth() &&
      d.getDate() === dt.getDate()
    )
      return { row: Math.floor(i / 7) + 2, col: (i % 7) + 1 };
  }
  return null;
}

export async function initMonthItems(
  isLoading: boolean,
  month: number,
  year: number,
  items: calendarItemsType[],
  days: any[]
): Promise<calendarItemsType[]> {
  items = await calendarData(isLoading, month, year, items);
  if (items !== undefined) {
    // eslint-disable-next-line no-self-assign
    items = items;
    for (const i of items) {
      const itemDate = new Date(i.date);
      const rc = findRowCol(itemDate, days);
      if (rc == null) {
        console.log("didn`t find date for ", i);
        i.startCol = i.startRow = 0;
      } else {
        i.startCol = rc.col;
        i.startRow = rc.row;
      }
    }
  }
  return items;
}

export function initMonth(days: any[], month: number, year: number) {
  days = [];
  const monthAbbrev = monthNames[month].slice(0, 3);
  const nextMonthAbbrev = monthNames[(month + 1) % 12].slice(0, 3);

  //	find the last Monday of the previous month
  const firstDay = new Date(year, month, 1).getDay();

  const daysInThisMonth = new Date(year, month + 1, 0).getDate();
  const daysInLastMonth = new Date(year, month, 0).getDate();

  const prevMonth = month == 0 ? 11 : month - 1;

  //	show the days before the start of this month (disabled) - always less than 7
  for (let i = daysInLastMonth - firstDay; i < daysInLastMonth; i++) {
    const d = new Date(prevMonth == 11 ? year - 1 : year, prevMonth, i + 1);
    days.push({
      name: "" + (i + 1),
      enabled: false,
      date: d
    });
  }

  //	show the days in this month (enabled) - always 28 - 31
  for (let i = 0; i < daysInThisMonth; i++) {
    const d = new Date(year, month, i + 1);
    if (i == 0)
      days.push({
        name: monthAbbrev + " " + (i + 1),
        enabled: true,
        date: d
      });
    else
      days.push({
        name: "" + (i + 1),
        enabled: true,
        date: d
      });
  }

  //	show any days to fill up the last row (disabled) - always less than 10
  for (let i = 0; days.length % 10; i++) {
    const d = new Date(month == 11 ? year + 1 : year, (month + 1) % 12, i + 1);
    if (i == 0)
      days.push({
        name: nextMonthAbbrev + " " + (i + 1),
        enabled: false,
        date: d
      });
    else
      days.push({
        name: "" + (i + 1),
        enabled: false,
        date: d
      });
  }
  return days;
}
