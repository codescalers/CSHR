export const clearUserData = (data: { [x: string]: any }) => {
  for (const field in data) {
    if (field == "birthday") {
      data[field] = new Date();
    } else if (field == "salary") {
      data[field] = {
        current_salary: { net: [], gross: [] },
        net_salary_before_joining: [],
        joining_salary: {
          net: [],
          gross: []
        },
        benefits: []
      };
    } else if (field == "reporting_to") {
      data[field] = [];
    } else if (field == "location") {
      data[field] = 0;
    } else {
      data[field] = "";
    }
  }
};

export const capitalize = (value: string): string => {
  return value[0].toLocaleUpperCase() + value.slice(1, value.length);
};

// Format the date to ISO string date then to date to be sent to the backend, valid format is yyyy-mm-dd
export const formatDate = (date: Date) => {
  if (typeof date != "string") {
    return date.toISOString().split("T")[0];
  }
  return date;
};
