
import calendarDataService from "../../services/axios/home/calendarDataService";
const main =
{
    "4": {
        "birthdates": [
            {
                "full_name": "Mazen swz",
                "email": "admin@gmail.com",
                "image": null
            },
            {
                "full_name": "Mahmud Emad",
                "email": "user@cshr.com",
                "image": null
            }
        ],
        "vactions": [
            {
                "reason": "leave_excuses",
                "from_date": "2022-09-04",
                "end_date": "2022-09-05",
                "status": "pending",
                "applying_user": {
                    "full_name": "Mahmud Emad",
                    "email": "user@cshr.com",
                    "image": null
                },
                "approval_user": {
                    "full_name": " ",
                    "email": "admin@gmail.com",
                    "image": null
                }
            },
            {
                "reason": "public_holidays",
                "from_date": "2022-09-04",
                "end_date": "2022-09-04T18:46:34.253276Z",
                "status": "rejected",
                "applying_user": {
                    "full_name": " ",
                    "email": "admin@gmail.com",
                    "image": null
                },
                "approval_user": {
                    "full_name": "Mahmud Emad",
                    "email": "user@cshr.com",
                    "image": null
                }
            },
            {
                "reason": "leave_excuses",
                "from_date": "2022-09-04T18:46:34.253276Z",
                "end_date": "2022-09-05T18:46:34.253276Z",
                "status": "approved",
                "applying_user": {
                    "full_name": " ",
                    "email": "admin@gmail.com",
                    "image": null
                },
                "approval_user": {
                    "full_name": "Mahmud Emad",
                    "email": "user@cshr.com",
                    "image": null
                }
            }
        ],
        "meetings": [
            {
                "invited_users": [
                    {
                        "full_name": " ",
                        "email": "admin@gmail.com",
                        "image": null
                    }
                ],
                "date": "2022-09-04T18:07:05Z",
                "meeting_link": "xs"
            }
        ],
        "events": [
            {
                "id": 1,
                "created_at": "2022-09-04T18:46:34.253198Z",
                "modified_at": "2022-09-04T18:46:34.253276Z",
                "name": "Sean Lowe",
                "description": "Soluta voluptas magnam impedit fugiat fugiat itaque voluptatem Sequi consequatur dolores rem voluptatem",
                "location": "Harum nostrud nisi occaecat rerum praesentium sit eveniet",
                "date": "2022-09-04T18:46:32Z",
                "people": [
                    2
                ]
            }
        ]
    },
    "5": {
        "vactions": [
            {
                "reason": "leave_excuses",
                "from_date": "2022-09-04",
                "end_date": "2022-09-05",
                "status": "pending",
                "applying_user": {
                    "full_name": "Mahmud Emad",
                    "email": "user@cshr.com",
                    "image": null
                },
                "approval_user": {
                    "full_name": " ",
                    "email": "admin@gmail.com",
                    "image": null
                }
            }
        ],
        "events": [
            {
                "id": 2,
                "created_at": "2022-09-04T18:47:03.467032Z",
                "modified_at": "2022-09-04T18:47:03.467058Z",
                "name": "Raya Mclean",
                "description": "Ut quasi dolores do ab facere voluptates non cumque dolorum",
                "location": "Est saepe ut fugiat beatae corrupti est consequat Voluptatibus",
                "date": "2022-09-05T18:46:58Z",
                "people": [
                    2
                ]
            }
        ]
    }
}



/* export default async function initCalendar() {
    let now = new Date();
    let year = now.getFullYear(); //	this is the month & year displayed
    let month = now.getMonth();
      let items = [{
           id: 1,
           title: "11:00 Task Early in month",
           className: "task--primary",
           description: "go to hossam office and discuss plan",
           date: new Date(y, m, randInt(6)),
           len: randInt(4) + 1,
           status: "expired",
       }]
    console.log(month + 1, year)
    const { data } = (await calendarDataService.initCalendar(month + 1, year));
    console.log("datam", data["6"]);

    let items = [];
    for (const dayStr in data) {
        let day: number = +dayStr;
        let date = new Date(year, month, day);
        console.log(date);

        for (let eventName in data[dayStr + ""]) {
            let eventArr = data[dayStr + ""][eventName];
            console.log(eventName);
            console.log(eventArr);
            for (let event of eventArr) {
                let len = 1;
                if (event.hasOwnProperty('end_date')) {
                    // len = ((new Date(event.get("end_date")).getDate() - date) + 1;
                    console.log("end-date" + event.end_date);
                }
                else {
                    len = 1;
                }
                let item = {
                    id: event.id,
                    title: event.name,
                    className: "task--primary",
                    description: event.description,
                    date: date,
                    len: 1,
                    status: "expired",
                }
                items.push(item);
            }
        }

        /*           let item = {};
                  let len = 1;
                  for (let event of eventArr) {
                         if (event.hasOwnProperty('end_date')) {
                             len = ((new Date(event.get("end_date")).getDate() - date) + 1;
                         }
                         else {
                             len = 1;
                         }
    }


    /*
                items.push({
                    id: event.id,
                    title: event.name,
                    className: "task--primary",
                    description: event.description,
                    date: date,
                    len: 1,
                    status: "expired",
                });

}
 */


//initCalendar();