export type eventNameType = "birthdates" | "vacations" | "events" | "meetings" | "others";

export type userType = {
    full_name: string,
    email: string,
    image: string,

}
export type birthDateItemType = {
    id: string,
    title: string,
    len: number,
    users: userType[],
    date: Date,
}
export type meetingItemType = {
    id: string,
    title: string,
    len: number,
    meeting_link: string,
    invited_users: userType[],
    date: Date,
}


export type eventItemType = {
    id: string,
    title: string,
    len: number,
    description: string,
    date: Date,
    people: userType[],
}
export type vacationItemType = {
    id: string,
    title: string,
    reason: string,
    len: number,
    applying_user: userType,
    approval_user: userType,
    status: string,
    date: Date,
}

export type classType = "task--primary" | "task--info" | "task--success" | "task--warning" | "task--danger" | "task--secondary" | "task--dark" | "task--light";

export type calendarItemType = meetingItemType | eventItemType | vacationItemType | birthDateItemType;


export type calendarOutputItemType = { "meeting": meetingItemType, "className": classType } |
{ "events": eventItemType, "className": classType } |
{ "vacations": vacationItemType, "className": classType } |
{ "birthDates": birthDateItemType, "className": classType };



export type calendarItemsType= (
    | {
        meetings: meetingItemType[];
        className: string;
        events?: undefined;
        vacations?: undefined;
        birthdates?: undefined;
      }
    | {
        events: eventItemType[];
        className: string;
        meetings?: undefined;
        vacations?: undefined;
        birthdates?: undefined;
      }
    | {
        vacations: vacationItemType[];
        className: string;
        meetings?: undefined;
        events?: undefined;
        birthdates?: undefined;
      }
    | {
        birthdates: birthDateItemType[];
        className: string;
        meetings?: undefined;
        events?: undefined;
        vacations?: undefined;
      }
  )[]
| [any, any, any, any]
| undefined;