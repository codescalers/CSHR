import { WeekendHolidaysEnum } from "./enums"
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