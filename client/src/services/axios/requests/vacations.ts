import axios from 'axios';
import http from "../http-common";

export default async function updateVacations(id: string,data:JSON) {
    

    let response = await  (await http.put(`vacations/edit/${id}/`,data))
    console.log(response)
}