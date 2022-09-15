import type { eventNameType, userType, vacationItemType } from "./types"
import { v4 as uuidv4 } from "uuid";

class Vacation {

    // to create the vacations list
    public vacationsItems(eventName: eventNameType, vacations: any, date: Date): vacationItemType[] {
        let items: vacationItemType[] = [];
        for (const vacation of vacations) {
            items = [...items, ...(this.vacationItem(eventName, vacation, date))];
        }
        return items;
    }

    // add number to current date to get the end date of the vacation
    private lastDayOFWeek(): Date {
        const today = new Date();
        const lastDay = new Date(today.setDate(today.getDate() - today.getDay() + 6));

        return lastDay;
    }

    // to create the vacation item
    private vacationItem(eventName: eventNameType, vacation: any, date: Date): vacationItemType[] {
        const id: string = uuidv4();
        const applying_user: userType = {
            id: vacation.applying_user.id,
            full_name: vacation.applying_user.full_name,
            email: vacation.applying_user.email,
            image: vacation.applying_user.image,
            team: vacation.applying_user.team,
            gender: vacation.applying_user.gender
        }
        const approval_user: userType = {
            id: vacation.approval_user.id,
            full_name: vacation.approval_user.full_name,
            email: vacation.approval_user.email,
            image: vacation.approval_user.image,
            team: vacation.approval_user.team,
            gender: vacation.approval_user.gender
        }
        let [from_year, from_month, from_day] = (vacation.from_date).split("-");
        let from_date = new Date(from_year, Number(from_month) - 1, from_day);
        let [endYear, endMonth, endDay] = (vacation.end_date).split("-");
        let end_date = new Date(endYear, Number(endMonth) - 1, endDay);
        const lastDay = this.lastDayOFWeek();

        let start = lastDay.getDate() - from_date.getDate();
        let end = end_date.getDate() - lastDay.getDate();

        if (end <= 0) {
            return [{
                id: id,
                title: "🌴" + eventName,
                reason: vacation.reason,
                len: end_date.getDate() - from_date.getDate() + 1,
                applying_user: applying_user,
                approval_user: approval_user,
                status: vacation.status,
                date: from_date,
                className: "task--warning",
                eventName: eventName,
                from_date: vacation.from_date,
                end_date: vacation.end_date,
                isStart: true,
                isBottom: false,

            }]
        }
        else {

            lastDay.setDate(lastDay.getDate() + 1)
            return [{
                id: id,
                title: "🌴" + eventName,
                reason: vacation.reason,
                len: start - 1,
                applying_user: applying_user,
                approval_user: approval_user,
                status: vacation.status,
                date: from_date,
                className: "task--warning",
                eventName: eventName,
                from_date: vacation.from_date,
                end_date: vacation.end_date,
                isStart: true,
                isBottom: false,
            },
            {
                id: uuidv4(),
                title: "",
                reason: vacation.reason,
                len: end,
                applying_user: applying_user,
                approval_user: approval_user,
                status: vacation.status,
                date: lastDay,
                className: "task--warning",
                eventName: eventName,
                from_date: vacation.from_date,
                end_date: vacation.end_date,
                isStart: true,
                isBottom: false,
            }
            ]
        }
    }
}


export default Vacation;