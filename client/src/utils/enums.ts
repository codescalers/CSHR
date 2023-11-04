export enum CalenderEventTyoe {
    vacation    = "vacation", 
    event       = "event",
    birthday    = "birthday",
    meeting     = "meeting"
}

export enum CalenderEventEmojeTyoe {
    vacation        = "🌴", 
    event           = "🎉",
    birthday        = "🎂",
    publicHoliday   = "💒",
    meeting         = "💼"
}

export enum UserTypeEnum {
    admin       = "Admin",
    supervisor  = "Supervisor",
    user        = "User"
}

export enum RequestStatus {
    approved    = "approved",
    rejected    = "rejected",
    pinding     = "pending"
};

export enum VacationTypeChoises {
    hr_letters   = "hr_letters",
    compensation = "compensation",
    vacations    = "vacations"
};

export enum EvaluationQuarter{
    JAN_MARCH   = "1 : 3",
    APR_JUN     = "4 : 6",
    JUL_SEP     = "7 : 9",
    OCT_DEC     = "10 : 12"
};

export enum WeekendHolidaysEnum{
    Friday_and_Saturday     = "Friday:Saturday",
    Saturday_and_Sunday     = "Saturday:Sunday",
    Sunday_and_Monday       = "Sunday:Monday",
    Monday_and_Tuesday      = "Monday:Tuesday",
    Tuesday_and_Wednesday   = "Tuesday:Wednesday",
    Wednesday_and_Thursday  = "Wednesday:Thursday",
    Thursday_and_Friday     = "Thursday:Friday",
};

export enum TeamEnum{
    BusinessDevelopment = "Business Development",
    Development = "Development",
    HRAndFinance = "HR & Finance",
    QA = "QA",
    Marketing = "Marketing",
    Operations = "Operations",
    Support = "Support",
};

export enum GenderEnum{
    Male        = "Male",
    Female      = "Female"
};