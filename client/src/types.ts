export type buttonType = "success" | "warning" | "error" | "info";
export type alertType = "success" | "warning" | "error" | "info";
export type requestStatus = "pending" | "approved" | "rejected";
export type requestTypeLabel = "Vacationa" | "HR Letter" | "Compensation" | "Danger";

export interface UserType {
    id: number;
    first_name: string;
    last_name: string;
    email: boolean;
    CreatedAt?: string;
    UpdatedAt?: string;
    DeletedAt?: string;

}


export interface SettingsType {
    name: string;
    email: string;
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
    type: requestTypeLabel;
    status: requestStatus;
    created_at: string;
}


