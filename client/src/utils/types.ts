export type buttonType = "success" | "warning" | "error" | "info";
export type alertType = "success" | "warning" | "error" | "info";
export type requestStatusType = "pending" | "approved" | "rejected";
export type UserType = "Admin" | "Supervisor" | "User";

export type requestLabelType =
  | "Vacation"
  | "HR Letter"
  | "Compensation"
  | "Danger";

export type eventNameType =
  | "vacation"
  | "meeting"
  | "event"
  | "birthday"
  | "public_holiday";

export interface GeneralUserInterface {
  id: number;
  full_name: string;
  first_name: string;
  background_color: string;
  last_name: string;
  email: string;
  gender: "Female" | "Male";
  team: string;
  image: string;
  address: string;
  birthday: string;
  created_at: string;
  job_title: string;
  telegram_link: string;
  skills: SkillType[];
  user_certificates: CertificateType[];
  reporting_to: TeamType[];
  location: OfficeType;
  user_type: UserType;
  remove_image?: boolean;
  is_active: boolean;
}

export interface SupervisorViewInterface extends GeneralUserInterface {
  mobile_number: string;
  social_insurance_number: string;
  user_evaluation: UserEvaluationType[];
  user_company_properties: CompanyPropertiesType[];
  salary: SalaryType;
}

export interface AdminViewInterface extends SupervisorViewInterface {
  salary: SalaryType;
}
export interface UserInterface extends SupervisorViewInterface {
  salary: SalaryType;
}

export interface PaginatedInterface<T> {
  results: T[];
  count: number;
  next: string;
  previous: string;
}
export interface NotifacationCreatedInterface {
  count: number;
}
export interface SettingsInterface {
  "primary-color": string;
  "secondary-color": string;
}

export interface RequestInterface {
  id: number;
  applying_user_id: number;
  approval_user_id: number;
  from_name: string;
  title: string;
  description: string;
  type: requestLabelType;
  status: requestStatusType;
  created_at: string;
}

export type OfficeType = {
  id: number;
  name: string;
  country: string;
};

export type NotificationType = {
  id: number;
};

export type TeamType = {
  id: number;
  full_name: string;
  email: string;
  image: string;
  team: string;
  job_title: string;
  user_type: string;
};

export type SupervisorType = {
  id: number;
  full_name: string;
  email: string;
  image: string;
  team: string;
  job_title: string;
  user_type: string;
};

export type SkillType = {
  id: number;
  name: string;
};

export type CertificateType = {
  id: number;
  name: string;
  certificate_link: string;
  user?: number;
  created_at?: Date;
  modified_at?: Date;
};

export type SalaryType = {
  current_salary: {
    net: number[];
    gross: number[];
  };
  joining_salary: {
    net: number[] | [];
    gross: number[] | [];
  };
  net_salary_before_joining: number[] | [];
  Benefits: number[] | [];
};

export type CompanyPropertiesType = {
  name: string;
  image_of: string;
  user_obj: TeamType;
};

export type UserEvaluationType = {
  user: number;
  quarter: string;
  link: string;
  score: number;
};
export interface IAuthStore {
  token?: string;
  refreshtoken?: string;
}

export type UserDocuments = {
  user: number;
  name: string;
  image: string;
  status: number;
};

export type SelectOptionType = {
  label: any;
  value: any;
  extraData?: any;
};

export type VacationBalanceType = {
  delete_old_balance?: boolean;
  user?: UserInterface;
  annual_leaves: number | BalanceValue;
  leave_excuses: number | BalanceValue;
  emergency_leaves: number | BalanceValue;
  public_holidays?: string[];
  year?: number;
  location?: OfficeType;
};

export type VacationBalanceValuesType = {
  annual_leaves: number;
  compensation: number;
  emergency_leaves: number;
  leave_excuses: number;
  sick_leaves: number;
  unpaid: number;
};

export type CalculateVacationBalanceType = {
  current: VacationBalanceValuesType;
  taked: VacationBalanceValuesType;
};

export type HRLetterType = {
  applying_user?: UserInterface;
  approval_user?: UserInterface;
  id?: number;
  addresses: string;
  with_date: boolean;
  with_salary_mentioned: boolean;
  from_date?: string | null;
  end_date?: string | null;
  status?: string;
};

export type CompensationType = {
  reason: string;
  from_date: string;
  end_date: string;
  applying_user?: UserInterface;
  approval_user?: UserInterface;
  status?: string;
  type?: string;
  id?: number;
};

export interface IVacationBalance {
  annual_leaves: number;
  leave_excuses: number;
  emergency_leaves: number;
  public_holidays: number[];
}

export type registeringData = {
  id: number;
  first_name: string;
  last_name: string;
  telegram_link: string;
  email: string;
  birthday: Date | string;
  mobile_number: string;
  address: string;
  password: string;
  location: number;
  team: string;
  salary: any;
  user_type: string;
  social_insurance_number: string;
  reporting_to: number[];
  image: string;
  gender: string;
  job_title: string;
};

export type loginDataType = {
  email: string;
  password: string;
};

export type loggingData = {
  refresh_token: string;
  access_token: string;
};

export type refreshData = {
  refresh: string;
  access: string;
};

export type dateType = {
  year: number;
  month: number;
  day: number;
  hour: number;
  minute: number;
};
export type userDataType = {
  id: number;
  full_name: string;
  email: string;
  image: string;
  team: string;
  gender: string;
  job_title: string;
};

export type holidaysDataType = {
  id: number;
  location: OfficeType;
  holiday_date: string;
  expired: boolean;
};

export type birthDateItemType = {
  id: number;
  title: string;
  len: number;
  users: userDataType[];
  date: Date;
  className: string;
  eventName: eventNameType;
  isStart: boolean;
  isBottom: boolean;
};
export type meetingItemType = {
  id: number;
  title: string;
  len: number;
  meeting_link: string;
  invited_users: userDataType[];
  host_user: userDataType;
  date: BackendParsedDate;
  parsedDate: dateType;
  className: string;
  eventName: eventNameType;
  isStart: boolean;
  isBottom: boolean;
  detailHeader?: string;
  detailContent?: string;
};

export type stackedImageType = {
  image: string;
  full_name?: string;
  gender?: string;
  team?: string;
};

export type BackendParsedDate = {
  year: number;
  month: number;
  day: number;
  hour: number;
  minute: number;
};

export type eventItemType = {
  id: number;
  name: string;
  description: string;
  date: Date;
  custom_people: userDataType[];
  location: string;
  from_time: string;
  end_time: string;
  from_date: BackendParsedDate;
  end_date: BackendParsedDate;
};

export type vacationItemType = {
  id: string;
  title: string;
  reason: string;
  applying_user: userDataType;
  approval_user: userDataType;
  status: string;
  from_date: Date;
  end_date: Date;
};

export type classType =
  | "task--primary"
  | "task--info"
  | "task--success"
  | "task--warning"
  | "task--danger"
  | "task--secondary"
  | "task--dark"
  | "task--light";

export type calendarItemType =
  | meetingItemType
  | eventItemType
  | vacationItemType
  | birthDateItemType;

export type calendarOutputItemType =
  | { meeting: meetingItemType; className: classType }
  | { events: eventItemType; className: classType }
  | { vacations: vacationItemType; className: classType }
  | { birthDates: birthDateItemType; className: classType };

export type calendarItemsType = {
  title: string;
  className: string;
  eventName: eventNameType;
  date: Date;
  len: number;
  isBottom?: boolean;
  startCol?: number;
  startRow?: number;
  id?: number;
  status?: string;
  detailHeader?: string;
  detailContent?: string;
  vacation?: vacationItemType[];
  meeting?: meetingItemType[];
  event?: eventItemType[];
  users?: userDataType[];
  holidays?: holidaysDataType[];
};

export type CalenderRequestFormResponseType = {
  message: string;
  isError: boolean;
};

export type BalanceValue = {
  reserved: number;
  all: number;
};

export interface VacationBalance {
  annual_leaves: BalanceValue;
  compensation: BalanceValue;
  emergency_leaves: BalanceValue;
  leave_excuses: BalanceValue;
  sick_leaves: BalanceValue;
  unpaid: BalanceValue;
}
