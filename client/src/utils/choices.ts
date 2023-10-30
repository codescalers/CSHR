import { WeekendHolidaysEnum, GenderEnum, TeamEnum, UserTypeEnum} from "./enums"

export const UserTypeChoice = [
    {
        label: UserTypeEnum.user,
        value: UserTypeEnum.user
    },
    {
        label: UserTypeEnum.supervisor,
        value: UserTypeEnum.supervisor
    },
    {
        label: UserTypeEnum.admin,
        value: UserTypeEnum.admin
    }
];

export const GenderChoice = [
    {
        label: GenderEnum.Male,
        value: GenderEnum.Male
    },
    {
        label: GenderEnum.Female,
        value: GenderEnum.Female
    }
];

export const TeamChoice = [
    {
        label: TeamEnum.BusinessDevelopment,
        value: TeamEnum.BusinessDevelopment
    },
    {
        label: TeamEnum.Development,
        value: TeamEnum.Development
    },
    {
        label: TeamEnum.HRAndFinance,
        value: TeamEnum.HRAndFinance
    },
    {
        label: TeamEnum.QA,
        value: TeamEnum.QA
    },
    {
        label: TeamEnum.Marketing,
        value: TeamEnum.Marketing
    },
    {
        label: TeamEnum.Operations,
        value: TeamEnum.Operations
    },
    {
        label: TeamEnum.Support,
        value: TeamEnum.Support
    },
];

export const weekendHolidaysChoices =  [
    { 
        label: WeekendHolidaysEnum.Friday_and_Saturday.replace(":", " and "),
        value: WeekendHolidaysEnum.Friday_and_Saturday
    },
    { 
        label: WeekendHolidaysEnum.Saturday_and_Sunday.replace(":", " and "),
        value: WeekendHolidaysEnum.Saturday_and_Sunday
    },
    { 
        label: WeekendHolidaysEnum.Sunday_and_Monday.replace(":", " and "),
        value: WeekendHolidaysEnum.Sunday_and_Monday
    },
    { 
        label: WeekendHolidaysEnum.Monday_and_Tuesday.replace(":", " and "),
        value: WeekendHolidaysEnum.Monday_and_Tuesday
    },
    { 
        label: WeekendHolidaysEnum.Tuesday_and_Wednesday.replace(":", " and "),
        value: WeekendHolidaysEnum.Tuesday_and_Wednesday
    },
    { 
        label: WeekendHolidaysEnum.Wednesday_and_Thursday.replace(":", " and "),
        value: WeekendHolidaysEnum.Wednesday_and_Thursday
    },
    { 
        label: WeekendHolidaysEnum.Thursday_and_Friday.replace(":", " and "),
        value: WeekendHolidaysEnum.Thursday_and_Friday
    },
];