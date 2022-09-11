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
    CreatedAt?: string;
    UpdatedAt?: string;
    DeletedAt?: string;
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


export type OfficeInterface = {
    id: number,
    name: string,
    country: string,
}



