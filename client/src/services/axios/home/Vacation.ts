import type { eventNameType, userType, vacationItemType } from "./types";
import { v4 as uuidv4 } from "uuid";

class Vacation {
	// to create the vacations list
	public vacationsItems(
		eventName: eventNameType,
		vacations: any,
		date: Date
	): vacationItemType[] {
		let items: vacationItemType[] = [];
		for (const vacation of vacations) {
			items = [...items, ...this.vacationItem(eventName, vacation, date)];
		}
		return items;
	}

	private lastDayOFWeek(startDate: Date): Date {
		const lastDay = new Date(
			startDate.setDate(startDate.getDate() - startDate.getDay() + 6)
		);
		return lastDay;
	}

	// to create the vacation item
	private vacationItem(
		eventName: eventNameType,
		vacation: any,
		date: Date
	): vacationItemType[] {
		const id: string = uuidv4();
		const applying_user: userType = {
			id: vacation.applying_user.id,
			full_name: vacation.applying_user.full_name,
			email: vacation.applying_user.email,
			image: vacation.applying_user.image,
			team: vacation.applying_user.team,
			gender: vacation.applying_user.gender,
		};
		const approval_user: userType = {
			id: vacation.approval_user.id,
			full_name: vacation.approval_user.full_name,
			email: vacation.approval_user.email,
			image: vacation.approval_user.image,
			team: vacation.approval_user.team,
			gender: vacation.approval_user.gender,
		};
		const [fromYear, fromMonth, fromDay] = vacation.from_date.split("-");
		const original_from_date = new Date(fromYear, Number(fromMonth) - 1, fromDay);
		const clone_from_date = new Date(fromYear, Number(fromMonth) - 1, fromDay);
		const incremental_from_date = new Date(
			fromYear,
			Number(fromMonth) - 1,
			fromDay
		);
		let weekly_from_date = new Date(fromYear, Number(fromMonth) - 1, fromDay);

		const [endYear, endMonth, endDay] = vacation.end_date.split("-");
		const end_date = new Date(endYear, Number(endMonth) - 1, endDay);
		const lastDay = this.lastDayOFWeek(clone_from_date);
		let items: vacationItemType[] = [];
		let length = 0;
		for (; true === true; ) {
			if (
				incremental_from_date.getDate() < end_date.getDate() &&
        incremental_from_date.getDate() < lastDay.getDate()
			) {
				length += 1;
				incremental_from_date.setDate(incremental_from_date.getDate() + 1);
			} else if (
				incremental_from_date.getDate() === end_date.getDate() ||
        incremental_from_date.getDate() === lastDay.getDate()
			) {
				length += 1;
				items = [
					...items,
					{
						id: uuidv4(),
						title: "🌴" + eventName,
						reason: vacation.reason,
						len: length,
						applying_user: applying_user,
						approval_user: approval_user,
						status: vacation.status,
						date: weekly_from_date,
						className: "task--warning",
						eventName: eventName,
						from_date: original_from_date,
						end_date: end_date,
						isStart: true,
						isBottom: false,
					},
				];
				if (incremental_from_date.getDate() === end_date.getDate()) {
					break;
				}
				incremental_from_date.setDate(incremental_from_date.getDate() + 1);
				weekly_from_date = new Date(incremental_from_date);
				lastDay.setDate(lastDay.getDate() + 7);
				length = 0;
			}
		}
		return items;
	}
}

export default Vacation;
