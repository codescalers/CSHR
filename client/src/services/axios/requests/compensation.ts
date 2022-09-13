import axios from 'axios';
import http from "../http-common";

export default async function updateCompensation(id: string,data:JSON | Object ) {
    let response = await  (await http.put(`compensation/edit/${id}/`,data))
    if (response.status == 202){
        return true;
    }
}