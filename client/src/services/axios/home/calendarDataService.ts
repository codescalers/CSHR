import http from "../http-common";
import itemHandler from "./itemHandler"
import type { eventNameType } from "./types"

class CalendarDataService {

    private itemHandler = itemHandler;

    private async getByMonthYearAPI(month: number, year: number) {
        try {
            return await (await http.get(`/home/?month=${month}&year=${year}`)).data;
        }
        catch (error) {
            throw new Error(`Error while fetching Calendar data ${error}`);
        }
    }


    public async initCalendar() {
        let now = new Date();
        let year = now.getFullYear(); //	this is the month & year displayed
        let month = now.getMonth();
        /*    let items = [{
               id: 1,
               title: "11:00 Task Early in month",
               className: "task--primary",
               description: "go to hossam office and discuss plan",
               date: new Date(y, m, randInt(6)),
               len: randInt(4) + 1,
               status: "expired",
           }] */

        console.log("today", month + 1, year)
        const { data } = (await this.getByMonthYearAPI(month + 1, year));
        console.log("datam", data["6"]);

        let items = [];

        for (const dayStr in data) {
            let day: number = +dayStr;
            let date = new Date(year, month, day);
            console.log(date);

            for (let eventName in data[dayStr + ""]) {
                let eventArr = data[dayStr + ""][eventName];
                items = this.itemHandler.createItems(eventName as eventNameType, eventArr);
                console.log("items", items);
            }

        }
    }
}

const calendarDataService = new CalendarDataService();

export default calendarDataService;