import type { eventNameType, meetingItemType } from "./types"

import { v4 as uuidv4 } from "uuid";


class Meeting {


    // to create the meetings list
    public meetingsItems(eventName: eventNameType, meetings: any, date: Date): meetingItemType[] {

        let items = [];
        for (const meeting of meetings) {
            items.push(this.meetingItem(eventName, meeting,date));
        }
        return items;
    }

    // to create the meeting Item
    private meetingItem(eventName: eventNameType, meeting: meetingItemType, date: Date): meetingItemType {
        const id: string = uuidv4();

        return {
            id: id,
            title: eventName,
            len: 1,
            date: date,
            meeting_link: meeting.meeting_link,
            invited_users: meeting.invited_users,

        }
    }
}

const meeting = new Meeting();

export default meeting;