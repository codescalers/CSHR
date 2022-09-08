import axios from 'axios';
import http from "../http-common";

export default async function getRequests() {
    

    let data=  (await http.get("requests/")).data.data;
    let request= []
    
    data.vacations.forEach(function(value){
        value.type= "Vacation"
        request.push(value)
    })
    data.compensations.forEach(function(value){
        value.type= "Compensation"
        request.push(value)
    })
    data.hr_letters.forEach(function(value){
        value.type= "HR letters"
        request.push(value)
    })
    console.log(request)
  
   return request
}
    

