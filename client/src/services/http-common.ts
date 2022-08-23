import axios from 'axios'

export default axios.create({
    baseURL: (process.env.APP_BASE_API_URL + ""),
    headers: {
        "Content-type": "application/json",
    },



});



//we use axios.create to create a new instance of Axios with a custom 
//config that has a base URL of  and a timeout of 1s.