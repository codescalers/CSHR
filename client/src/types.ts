export type buttonType = "success" | "warning" | "error" | "info";
export type alertType = "success" | "warning" | "error" | "info";
export type requestStatusType = "pending" | "approved" | "rejected";
export type UserType = "Admin" | "Supervisor" | "User";
export type requestLabelType =
  | "Vacation"
  | "HR Letter"
  | "Compensation"
  | "Danger";

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
export interface NotifacationCreatedInterface{
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
  delete_old_balance: boolean;
  user: UserInterface;
  annual_leaves: number;
  leave_excuses: number;
  emergency_leaves: number;
  public_holidays?: number[];
};

export type HRLetterType = {
  addresses: string;
  with_date: boolean;
  with_salary_mentioned: boolean;
  from_date?: string|null;
  end_date?: string|null;
};

export type CompensationType = {
  reason: string;
  from_date: string;
  end_date: string;
  applying_user?: GeneralUserInterface | number;
  approval_user?: GeneralUserInterface;
  status?: string;
  type?: string;
  id?: number;
};

export interface IVacationBalance {
  annual_leaves: number;
  leave_excuses: number;
  emergency_leaves: number;
  public_holidays: number[];
};

export type registeringData = {
  id: number;
  first_name: string;
  last_name: string;
  telegram_link: string;
  email: string;
  birthday: Date;
  mobile_number: string;
  address: string;
  password: string;
  location: number;
  team: string;
  salary: any;
  user_type: string;
  social_insurance_number: string;
  reporting_to: number[];
  image: HTMLImageElement;
  gender: string ;
  job_title:string;
};