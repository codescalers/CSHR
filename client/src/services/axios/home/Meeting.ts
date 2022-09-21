import type { eventNameType, meetingItemType, dateType } from "./types";

import { v4 as uuidv4 } from "uuid";

class Meeting {
	// to create the meetings list
	public meetingsItems(
		eventName: eventNameType,
		meetings: any,
		date: Date
	): meetingItemType[] {
		const items = [];
		for (const meeting of meetings) {
			items.push(this.meetingItem(eventName, meeting, date));
		}
		return items;
	}

	// to create the meeting Item
	private meetingItem(
		eventName: eventNameType,
		meeting: meetingItemType,
		date: Date
	): meetingItemType {
		const id: string = uuidv4();
		const today = new Date();
		const parsedDate = meeting.date as unknown as dateType;
		let difficulty = {};
		if (today.toDateString() === date.toDateString()) {
			difficulty = {
				detailHeader: "Meeting @" + parsedDate.hour + ":" + parsedDate.minute,
				detailContent: `<a href="${meeting.meeting_link}" target="_blank" rel="noopener noreferrer">${meeting.meeting_link}</a>`,
			};
		}

		return {
			id: id,
			title: "💼meeting",
			len: 1,
			date: date,
			parsedDate: parsedDate,
			meeting_link: meeting.meeting_link,
			invited_users: meeting.invited_users,
			host_user: meeting.host_user,
			className: "task--danger",
			eventName: eventName,
			isStart: false,
			isBottom: true,
			...difficulty,
		};
	}
}

const meeting = new Meeting();

export default meeting;
