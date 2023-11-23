export const clearUserData = (data) => {
    for (const field in data) {
        if (field == "birthday") {
            data[field] = new Date();
        }
        else if (field == "salary") {
            data[field] = {
                current_salary: { net: [], gross: [] },
                net_salary_before_joining: [],
                joining_salary: {
                    net: [],
                    gross: [],
                },
                benefits: [],
            };
        }
        else if (field == "reporting_to") {
            data[field] = [];
        }
        else if (field == "location") {
            data[field] = 0;
        }
        else {
            data[field] = "";
        }
    }
};
//# sourceMappingURL=helpers.js.map