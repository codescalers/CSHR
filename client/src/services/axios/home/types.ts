export type eventNameType = "birthdates" | "vactions" | "events" | "meetings" | "others";

export type userBirthDateType = {
    full_name: string,
    email: string,
    image: string,

}
export type birthDateType = {
    id: string,
    title: string,
    len: number,
    className: string,
    users: userBirthDateType[],
    date: Date,
}