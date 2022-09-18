import axios from 'axios'

export default axios.create({
    baseURL: (process.env.APP_BASE_API_URL + "api/"),
    headers: {
        "Content-type": "application/json",
        'Authorization': `Bearer ${(process.env.TEMP_TOKEN + "") || localStorage.getItem("token")}`
    },
});
