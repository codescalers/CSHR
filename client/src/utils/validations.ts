import type { CalenderRequestFormResponseType } from "./types";
export const validateEmail = (e: any): boolean => {
  const re =
    /^(([^<>()\\[\]\\.,;:\s@"]+(\.[^<>()\\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return !re.test(String(e.target.value).toLowerCase());
};

export const validatePassword = (e: any): boolean => {
  if (e.target.value.length >= 8) return false;
  return true;
};

export const validateName = (e: any): boolean => {
  const re = /^[a-zA-Z]+$/;
  return !re.test(String(e.target.value));
};

export function validateSpcialEmptyString(e: any): boolean {
  return e.target.value.length < 2 ? true : false;
}

export const validateLink = (e: any): boolean => {
  const urlPattern = new RegExp(
    "^(https?:\\/\\/)?" + // validate protocol
      "((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|" + // validate domain name
      "((\\d{1,3}\\.){3}\\d{1,3}))" + // validate OR ip (v4) address
      "(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*" + // validate port and path
      "(\\?[;&a-z\\d%_.~+=-]*)?" + // validate query string
      "(\\#[-a-z\\d_]*)?$",
    "i"
  ); // validate fragment locator
  return !urlPattern.test(String(e.target.value));
};

export const validatePhoneNumber = (e: any): boolean => {
  if (e.target.value.match(/\b(\d{10,15})$/)) return false;
  return true;
};

export const validateTelegramLink = (e: any): boolean => {
  if (e.target.value[0] == "@") return false;
  return true;
};

export const validateSalary = (e: any): boolean => {
  if (e.target.value > 0) return false;
  return true;
};

export const validateBirthday = (e: any): boolean => {
  const date = new Date(e.target.value);
  const today = new Date();
  if (date.getFullYear() < today.getFullYear()) {
    return false;
  }
  return true;
};

export const validateBackgroundColor = (e: any): boolean => {
  if (e.target.value[0] == "#" && isNaN(e.target.value.slice(1, -1)))
    return false;
  return true;
};

export const validateStartEndDates = (startDate: Date, endDate: Date) => {
  const response: CalenderRequestFormResponseType = {
    message: undefined,
    isError: false
  };

  endDate.setHours(0, 0, 0, 0); // Set the time to midnight for accurate comparison

  if (startDate > endDate) {
    response.message = "End date cannot be < start date.";
    response.isError = true;
  }

  return response;
};

export function isValidDate(d: any) {
  if (d.split("-").length != 3) {
    return false;
  } else {
    try {
      const date = new Date(d);
      return date.getDate() ? true : false;
    } catch {
      return false;
    }
  }
}
