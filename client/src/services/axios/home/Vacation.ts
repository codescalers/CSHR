import type { eventNameType, userType, vacationItemType } from "./types"
import { v4 as uuidv4 } from "uuid";

class Vacation {

    // to create the vacations list
    public vacationsItems(eventName: eventNameType, vacations: any, date: Date): vacationItemType[] {
        let items: vacationItemType[] = [];
        for (const vacation of vacations) {
            items.push(this.vacationItem(eventName, vacation, date));
        }
        return items;
    }
    // to create the vacation item
    private vacationItem(eventName: eventNameType, event: any, date: Date): vacationItemType {
        const id: string = uuidv4();

        const applying_user: userType = {
            id: event.applying_user.id,
            full_name: event.applying_user.full_name,
            email: event.applying_user.email,
            image: event.applying_user.image,
            team: event.applying_user.team,
            gender: event.applying_user.gender
        }
        const approval_user: userType = {
            id: event.approval_user.id,
            full_name: event.approval_user.full_name,
            email: event.approval_user.email,
            image: event.approval_user.image,
            team: event.approval_user.team,
            gender: event.approval_user.gender
        }
        console.log("event", event)

        return {
            id: id,
            title: "🌴" + eventName,
            reason: event.reason,
            len: 1,
            applying_user: applying_user,
            approval_user: approval_user,
            status: event.status,
            date: date,
            className: "task--warning",
            eventName: eventName,
            isStart: true,
            isBottom: false,

        }
    }
}


export default Vacation;