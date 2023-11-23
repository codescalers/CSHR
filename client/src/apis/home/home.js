/* eslint-disable prefer-const */
import http from "../../utils/axios";
class HomePage {
    constructor() {
        this.errorMessage = "Error in Office Data Service: ";
    }
    async eventCalendarAPI(month, year) {
        // Request to get all events that related to exactly the same month, year.
        try {
            return await (await http.get(`/home/?month=${month}&year=${year}`)).data;
        }
        catch (error) {
            throw new Error(error.response.data.message || error.response.data.detail);
        }
    }
    async postEvent(e) {
        try {
            if (!e.name ||
                // !e.people ||
                // e.people.length === 0 ||
                !e.end_date ||
                // !e.location ||
                !e.end_time ||
                !e.from_time)
                throw new Error("Invalid data");
            // if (e.people.length === 0) throw new Error("No invited users");
            let [fromHour, fromMinute] = e.from_time.split(":");
            const [fromYear, fromMonth, fromDay] = e.from_date.split("-");
            let [endHour, endMinute] = e.end_time.split(":");
            const [endYear, endMonth, endDay] = e.end_date.split("-");
            if (fromHour == "00") {
                fromHour = "12";
            }
            if (endHour == "00") {
                endHour = "12";
            }
            const data = {
                people: [],
                from_date: {
                    year: Number(fromYear),
                    month: Number(fromMonth),
                    day: Number(fromDay),
                    hour: Number(fromHour),
                    minute: Number(fromMinute),
                },
                end_date: {
                    year: Number(endYear),
                    month: Number(endMonth),
                    day: Number(endDay),
                    hour: Number(endHour),
                    minute: Number(endMinute),
                },
                name: e.name,
                description: e.description,
                location: e.location,
            };
            return await http.post("/event/", JSON.stringify(data));
        }
        catch (error) {
            console.error(`${this.errorMessage} Error while posting event data ${error}`);
            return error;
        }
    }
    async postMeeting(e) {
        try {
            if (!e.hostedUserID || !e.invitedUsers || !e.meetingLink || !e.time || !e.date)
                throw new Error("Invalid data");
            // if (e.invitedUsers.length === 0) throw new Error("No invited users");
            if (e.invitedUsers.includes(e.hostedUserID))
                throw new Error("Hosted user is also invited");
            let [hour, minute] = e.time.split(":");
            if (hour == "00") {
                hour = "12";
            }
            const [year, month, day] = e.date.split("-");
            return await http.post("/meeting/", JSON.stringify({
                host_user: e.hostedUserID,
                invited_users: e.invitedUsers,
                date: {
                    year: Number(year),
                    month: Number(month),
                    day: Number(day),
                    hour: Number(hour),
                    minute: Number(minute),
                },
                meeting_link: e.meetingLink,
                location: e.location,
            }));
        }
        catch (error) {
            console.error(`${this.errorMessage} Error while posting meeting data ${error}`);
            return error;
        }
    }
}
const homePage = new HomePage();
export default homePage;
//# sourceMappingURL=home.js.map