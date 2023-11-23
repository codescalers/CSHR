import { GenderEnum, TeamEnum, UserTypeEnum, WeekendHolidaysEnum } from "./enums";

export const UserTypeChoice = [
  {
    label: UserTypeEnum.user,
    value: UserTypeEnum.user,
  },
  {
    label: UserTypeEnum.supervisor,
    value: UserTypeEnum.supervisor,
  },
  {
    label: UserTypeEnum.admin,
    value: UserTypeEnum.admin,
  },
];

export const GenderChoice = [
  {
    label: GenderEnum.Male,
    value: GenderEnum.Male,
  },
  {
    label: GenderEnum.Female,
    value: GenderEnum.Female,
  },
];

export const TeamChoice = [
  {
    label: TeamEnum.BusinessDevelopment,
    value: TeamEnum.BusinessDevelopment,
  },
  {
    label: TeamEnum.Development,
    value: TeamEnum.Development,
  },
  {
    label: TeamEnum.HRAndFinance,
    value: TeamEnum.HRAndFinance,
  },
  {
    label: TeamEnum.QA,
    value: TeamEnum.QA,
  },
  {
    label: TeamEnum.Marketing,
    value: TeamEnum.Marketing,
  },
  {
    label: TeamEnum.Operations,
    value: TeamEnum.Operations,
  },
  {
    label: TeamEnum.Support,
    value: TeamEnum.Support,
  },
];

export const weekendHolidaysChoices = [
  {
    label: WeekendHolidaysEnum.Friday_and_Saturday.replace(":", " and "),
    value: WeekendHolidaysEnum.Friday_and_Saturday,
  },
  {
    label: WeekendHolidaysEnum.Saturday_and_Sunday.replace(":", " and "),
    value: WeekendHolidaysEnum.Saturday_and_Sunday,
  },
];
