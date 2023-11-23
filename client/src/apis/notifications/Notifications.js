import http from "../../utils/axios";
class NotificationService {
    constructor() {
        this.errorMessage = "Error in Notifacation Service: ";
    }
    async getAll() {
        try {
            const { data, status, statusText } = await http.get("/notifications/");
            if (status !== 200) {
                throw new Error("Error in getting notifications with status " + status + " wtih status text : " + statusText);
            }
            return data.results;
        }
        catch (err) {
            console.error(this.errorMessage + err);
            throw new Error(err);
        }
    }
}
const notificationsAPI = new NotificationService();
export default notificationsAPI;
//# sourceMappingURL=Notifications.js.map