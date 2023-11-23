import http from "../../utils/axios";
class Requests {
    async getRequests() {
        // Request to get all requests from the server then loop over each type.
        const data = (await http.get("requests/")).data.results;
        const request = [];
        data.vacations.forEach(function (value) {
            value.type = "Vacations";
            request.push(value);
        });
        data.hr_letters.forEach(function (value) {
            value.type = "HR letters";
            request.push(value);
        });
        data.compensations.forEach(function (value) {
            value.type = "Compensations";
            request.push(value);
        });
        data.official_docs.forEach(function (value) {
            value.type = "Official documents";
            request.push(value);
        });
        document.body.style.cursor = "default";
        return request;
    }
    async approve(incomingData, id) {
        // Request to approve request with exact id.
        const type = incomingData.type.toLowerCase().replace(" ", "_");
        try {
            return await http.put(`/${type}/approve/${id}/`, incomingData);
        }
        catch (err) {
            throw new Error(err.response.data.message);
        }
    }
    async reject(incomingData, id) {
        // Request to reject request with exact id.
        const type = incomingData.type.toLowerCase().replace(" ", "_");
        try {
            return await http.put(`/${type}/reject/${id}/`, incomingData);
        }
        catch (err) {
            throw new Error(err.response.data.message);
        }
    }
    async delete(incomingData) {
        // Request to delete request with exact id.
        try {
            return await http.delete(`/${incomingData.type.toLowerCase()}/${incomingData.id}/`);
        }
        catch (err) {
            throw new Error(err.response.data.message);
        }
    }
}
const requestTypes = new Requests();
export default requestTypes;
//# sourceMappingURL=Requests.js.map