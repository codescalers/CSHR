import axios from 'axios';
import http from "../http-common";

export default async function updateLetters(id: string,data:JSON | Object) {
    let response = await  (await http.put(`hrletter/edit/${id}/`,data))
    if (response.status == 202){
        return true;
    }
}