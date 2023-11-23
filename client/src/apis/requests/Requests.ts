import http from "../../utils/axios";

class Requests {
  public async getRequests() {
    // Request to get all requests from the server then loop over each type.
    const data = (await http.get("requests/")).data.results;
    const request: any = [];

    data.vacations.forEach(function (value: any) {
      value.type = "Vacations";
      request.push(value);
    });

    data.hr_letters.forEach(function (value: any) {
      value.type = "HR letters";
      request.push(value);
    });

    data.compensations.forEach(function (value: any) {
      value.type = "Compensations";
      request.push(value);
    });

    data.official_docs.forEach(function (value: any) {
      value.type = "Official documents";
      request.push(value);
    });

    document.body.style.cursor = "default";
    return request;
  }

  public async approve(incomingData: any, id: number) {
    // Request to approve request with exact id.
    const type: string = incomingData.type.toLowerCase().replace(" ", "_");
    try {
      return await http.put(`/${type}/approve/${id}/`, incomingData);
    } catch (err: any) {
      throw new Error(err.response.data.message);
    }
  }

  public async reject(incomingData: any, id: number) {
    // Request to reject request with exact id.
    const type: string = incomingData.type.toLowerCase().replace(" ", "_");
    try {
      return await http.put(`/${type}/reject/${id}/`, incomingData);
    } catch (err: any) {
      throw new Error(err.response.data.message);
    }
  }
  public async delete(incomingData: any) {
    // Request to delete request with exact id.
    try {
      return await http.delete(`/${incomingData.type.toLowerCase()}/${incomingData.id}/`);
    } catch (err: any) {
      throw new Error(err.response.data.message);
    }
  }
}

const requestTypes = new Requests();
export default requestTypes;
