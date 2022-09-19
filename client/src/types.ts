export type buttonType = "success" | "warning" | "error" | "info";
export type alertType = "success" | "warning" | "error" | "info";
export type requestStatusType = "pending" | "approved" | "rejected";
export type requestLabelType = "Vacationa" | "HR Letter" | "Compensation" | "Danger";

export interface UserInterface {
    id: number;
    full_name: string;
    email: string;
    phone_number: string;
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
    telegram_link: string,
    skills: number[],
    user_certificates: number[],
    reporting_to: number[],

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
    id: number,
    name: string,
    country: string,
}

export type NotificationType = {
    id: number,
}


export type TeamType = {
    id: number,
    name: string,
    office: number,
    members: number[],
    managers: number[],
    CreatedAt?: string,
    UpdatedAt?: string,
    DeletedAt?: string,
}

export type SkillType = {
    id: number,
    name: string,
    CreatedAt?: string,
    UpdatedAt?: string,
    DeletedAt?: string,
}

export type CertificateType = {
    id: number,
    name: string,
    CreatedAt?: string,
    UpdatedAt?: string,
    DeletedAt?: string,
}

