import http from "../../utils/axios";

class NotificationService {
  errorMessage = "Error in Notifacation Service: ";
  public async getAll() {
    try {
      const { data, status, statusText } = await http.get("/notifications/");
      if (status !== 200) {
        throw new Error(
          "Error in getting notifications with status " +
            status +
            " wtih status text : " +
            statusText
        );
      }
      return data.results;
    } catch (err: any) {
      console.error(this.errorMessage + err);
      throw new Error(err);
    }
  }
}

const notificationsAPI = new NotificationService();
export default notificationsAPI;
