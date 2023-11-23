import http from "../../utils/axios";
class Events {
    // Class Meetings data service to request to meetings endpoints.
    async exact(day) {
        // Request to get all meetings on an axact day.
        try {
            return await http.get(`event/exact/?day=${day}`);
        }
        catch (err) {
            throw new Error(err.response.data.message);
        }
    }
}
const eveentsAPI = new Events();
export default eveentsAPI;
//# sourceMappingURL=Event.js.map