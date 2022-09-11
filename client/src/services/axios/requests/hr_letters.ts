import axios from 'axios';
import http from "../http-common";

export default async function updateLetters(id: string,data:JSON) {
    let response = await  (await http.put(`hrletter/edit/${id}/`,data))
    console.log(response)
}