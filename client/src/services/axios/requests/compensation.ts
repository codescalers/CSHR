import axios from 'axios';
import http from "../http-common";

export default async function updateCompensation(id: string,data:JSON) {
    let response = await  (await http.put(`compensation/${id}/`,data))
    console.log(response)
}