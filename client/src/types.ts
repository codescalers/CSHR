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
    net: number[];
    gross: number[];
  };
  net_salary_before_joining?: number[];
  Benefits?: number[];
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

export type VacationBalanceType = {
  annual_leaves: number;
  leave_execuses: number;
  emergency_leaves: number;
  public_holidays?: number[];
}

export interface IVacationBalance {
  annual_leaves: number;
  leave_execuses: number;
  emergency_leaves: number;
  public_holidays: number[];
}
