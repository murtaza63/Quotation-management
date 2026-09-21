import api from "./axios";

export interface LoginResponse {
    access_token: string;
    token_type: string;
}

export const loginUser = async (
    username: string,
    password: string
): Promise<LoginResponse> => {
    const formData = new URLSearchParams();

    formData.append("username", username);
    formData.append("password", password);

    const response = await api.post<LoginResponse>(
        "/auth/login",
        formData,
        {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
        }
    );

    localStorage.setItem("access_token", response.data.access_token);

    return response.data;
};