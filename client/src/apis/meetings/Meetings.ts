import http from "../../utils/axios";

class Meetings {
  // Class Meetings data service to request to meetings endpoints.
  public async exact(year: number, month: number, day: number) {
    // Request to get all meetings on an axact day.
    try {
      return await http.get(
        `meeting/exact/?year=${year}&&month=${month}&&day=${day}`
      );
    } catch (err: any) {
      throw new Error(err.response.data.message);
    }
  }
}

const meetingsAPI = new Meetings();
export default meetingsAPI;
