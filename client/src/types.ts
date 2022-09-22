export type buttonType = "success" | "warning" | "error" | "info";
export type alertType = "success" | "warning" | "error" | "info";
export type requestStatusType = "pending" | "approved" | "rejected";
export type requestLabelType =
  | "Vacation"
  | "HR Letter"
  | "Compensation"
  | "Danger";

export interface GeneralUserInterface {
  id: number;
  full_name: string;
  email: string;
  team: string;
  password?: string;
  role: string;
  image: string;
  gender: "Female" | "Male";
  address: string;
  birthday: string;
  CreatedAt?: string;
  UpdatedAt?: string;
  DeletedAt?: string;
  job_title: string;
  telegram_link: string;
  skills: SkillType[];
  user_certificates: CertificateType[];
  reporting_to: number[];
}





export interface SupervisorViewType extends GeneralUserInterface {
  mobile_number: string;
  social_insurance_number: string;
  location: number;
  user_evaluations: [];
  user_company_properties: number[],
}

export interface AdminViewType extends SupervisorViewType {
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

export type SalaryType =
  {
    current_salary: {
      net: number[],
      gross: number[]
    },
    joining_salary: {
      net: number[],
      gross: number[]
    }
  }