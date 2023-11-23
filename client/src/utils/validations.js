export const validateEmail = (e) => {
    const re = /^(([^<>()\\[\]\\.,;:\s@"]+(\.[^<>()\\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return !re.test(String(e.target.value).toLowerCase());
};
export const validatePassword = (e) => {
    if (e.target.value.length >= 8)
        return false;
    return true;
};
export const validateName = (e) => {
    const re = /^[a-zA-Z]+$/;
    return !re.test(String(e.target.value));
};
export function validateSpcialEmptyString(e) {
    if (e.target.value.length < 2)
        return true;
}
export const validateLink = (e) => {
    const urlPattern = new RegExp("^(https?:\\/\\/)?" + // validate protocol
        "((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|" + // validate domain name
        "((\\d{1,3}\\.){3}\\d{1,3}))" + // validate OR ip (v4) address
        "(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*" + // validate port and path
        "(\\?[;&a-z\\d%_.~+=-]*)?" + // validate query string
        "(\\#[-a-z\\d_]*)?$", "i"); // validate fragment locator
    return !urlPattern.test(String(e.target.value));
};
export const validatePhoneNumber = (e) => {
    if (e.target.value.match(/\b(\d{10,15})$/))
        return false;
    return true;
};
export const validateTelegramLink = (e) => {
    if (e.target.value[0] == "@")
        return false;
    return true;
};
export const validateSalary = (e) => {
    if (e.target.value > 0)
        return false;
    return true;
};
export const validateBirthday = (e) => {
    const date = new Date(e.target.value);
    const today = new Date();
    if (date.getFullYear() < today.getFullYear()) {
        return false;
    }
    return true;
};
export const validateBackgroundColor = (e) => {
    if (e.target.value[0] == "#" && isNaN(e.target.value.slice(1, -1)))
        return false;
    return true;
};
//
export const validateStartEndDates = (date, startDate, endDate) => {
    const response = {
        message: "Success!",
        isError: false,
    };
    const validateStartDate = new Date(startDate);
    const validateEndDate = new Date(endDate);
    const now = new Date();
    const check = Date.parse(date);
    if (!check ||
        startDate.split("-").length != 3 ||
        endDate.split("-").length != 3 ||
        startDate.split("-")[2] == "" ||
        endDate.split("-")[2] == "" ||
        +startDate.split("-")[2] == 0 ||
        +endDate.split("-")[2] == 0 ||
        +startDate.split("-")[1] > 12 ||
        +startDate.split("-")[1] < 1 ||
        +endDate.split("-")[1] > 12 ||
        +endDate.split("-")[1] < 1) {
        response.message = "Format is invalid";
        response.isError = true;
        return response;
    }
    if (validateStartDate.getFullYear() == validateEndDate.getFullYear() &&
        validateStartDate.getMonth() > validateEndDate.getMonth()) {
        response.message = "Start month must be > end month.";
        response.isError = true;
        return response;
    }
    if (validateEndDate.getFullYear() - now.getFullYear() >= 3) {
        response.message = "No one can take it :D";
        response.isError = true;
        return response;
    }
    if (validateStartDate.getMonth() == validateEndDate.getMonth() &&
        validateStartDate.getFullYear() == validateEndDate.getFullYear() &&
        validateStartDate.getDate() > validateEndDate.getDate()) {
        response.message = "Start day must be > end day.";
        response.isError = true;
        return response;
    }
    if (validateStartDate.getDate() < 1 || validateEndDate.getDate() < 1) {
        response.message = "The day is invalid.";
        response.isError = true;
        return response;
    }
    if (validateStartDate.getFullYear() < now.getFullYear()) {
        response.message = "Start year must be > the current year.";
        response.isError = true;
        return response;
    }
    if (validateEndDate.getFullYear() < now.getFullYear()) {
        response.message = "End year must be > the current year.";
        response.isError = true;
        return response;
    }
    if (validateEndDate.getFullYear() < validateStartDate.getFullYear()) {
        response.message = "End year must be < start year.";
        response.isError = true;
        return response;
    }
    return response;
};
export function isValidDate(d) {
    if (d.split("-").length != 3) {
        return false;
    }
    else {
        try {
            const date = new Date(d);
            return date.getDate() ? true : false;
        }
        catch (_a) {
            return false;
        }
    }
}
//# sourceMappingURL=validations.js.map