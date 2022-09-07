import type { eventNameType, meetingItemType } from "./types"

import { v4 as uuidv4 } from "uuid";


class Meeting {
    private date: Date;


    // to set the date
    public set setDate(date: Date) {
        this.date = date;
    }

    // to create the meetings list
    public meetingsItems(eventName: eventNameType, meetings: any): meetingItemType[] {

        let items = [];
        for (const meeting of meetings) {
            items.push(this.meetingItem(eventName, meeting));
        }
        return items;
    }

    // to create the meeting Item
    private meetingItem(eventName: eventNameType, meeting: meetingItemType): meetingItemType {
        const id: string = uuidv4();


        return {
            id: id,
            title: eventName,
            len: 1,
            date: this.date,
            meeting_link: meeting.meeting_link,
            invited_users: meeting.invited_users,

        }
    }
}

const meeting = new Meeting();

export default meeting;