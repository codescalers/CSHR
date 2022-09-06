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
    className: string,
    users: userType[],
    date: Date,
}
export type meetingItemType = {
    id: string,
    title: string,
    len: number,
    meeting_link: string
    className: string,
    invited_users: userType[],
    date: Date,
}


export type eventItemType = {
    id: string,
    title: string,
    len: number,
    description: string,
    className: string,
    date: Date,
}
export type vacationItemType = {
    id: string,
    title: string,
    reason: string,
    len: number,
    applying_user: userType,
    approval_user: userType,
    className: string,
    status: string,
    date: Date,
}
export type calendarItemType = userType | eventItemType | vacationItemType | birthDateItemType ;