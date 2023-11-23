import http from "../../utils/axios";

class Events {
  // Class Meetings data service to request to meetings endpoints.
  public async exact(day: number) {
    // Request to get all meetings on an axact day.
    try {
      return await http.get(`event/exact/?day=${day}`);
    } catch (err: any) {
      throw new Error(err.response.data.message);
    }
  }
}

const eveentsAPI = new Events();
export default eveentsAPI;
