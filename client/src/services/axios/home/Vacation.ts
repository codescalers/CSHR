import type { eventNameType, userType, vacationItemType } from "./types"
import { v4 as uuidv4 } from "uuid";

class Vacation {
    private date: Date;
    constructor(private cssClassMapping: (eventName: eventNameType) => string) { }

    // to create the vacations list
    public vacationsItems(eventName: eventNameType, vacations: any): vacationItemType[] {
        let items: vacationItemType[] = [];
        for (const vacation of vacations) {
            items.push(this.vacationItem(eventName, vacation));
        }
        return items;
    }
    // to create the vacation item
    private vacationItem(eventName: eventNameType, event: any): vacationItemType {
        const id: string = uuidv4();

        const applying_user: userType = {
            full_name: event.applying_user.full_name,
            email: event.applying_user.email,
            image: event.applying_user.image,
        }
        const approval_user: userType = {
            full_name: event.approval_user.full_name,
            email: event.approval_user.email,
            image: event.approval_user.image,
        }
        return {
            id: id,
            title: eventName,
            reason: event.reason,
            len: 1,
            applying_user: applying_user,
            approval_user: approval_user,
            className: this.cssClassMapping(eventName),
            status: event.status,
            date: this.date,
        }
    }

    // to set the date
    public set setDate(date: Date) {
        this.date = date;
    }
}


export default Vacation;