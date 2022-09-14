import axios from 'axios';
import http from "../http-common";

export default async function updateVacations(id: string,data:Object | JSON)   {
    

    let response =   (await http.put(`vacations/edit/${id}/`,data))
    if (response.status == 202){
        return true
    }
}