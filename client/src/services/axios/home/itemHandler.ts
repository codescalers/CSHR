type eventNameType = "birthdates" | "vactions" | "events" | "meetings" | "others";


class ItemHandler {
    public createItem(eventName: eventNameType, event: any) {
        let items = [];



        switch (eventName) {
            case "events":
                items = this.events(event);
                break;
            case "birthdates":
                items = this.birthDates(event);
                break;
            case "meetings":
                items = this.meetings(event);

        }


        return items;
    }

    private events(eventName: string, event: any) {

    }
    private event(eventName: string, event: any) {
        return {
            id: event.id,
            title: event.name,
            description: event.description,
            len: 1,
            className: this.cssClassMapping(eventName)
        }
    }



    private birthDates(event: any) {
        return {
            id: event.id,
            title: event.name,
            description: event.description,
            len: 1,
        }
    }
    private birthDate(event: any) {
        return {
            id: event.id,
            title: event.name,
            description: event.description,
            len: 1,
        }
    }

    private meetings(event: any) {
        return {
            id: event.id,
            title: event.name,
            description: event.description,
            len: 1,
        }
    }




    private cssClassMapping(eventName: string) {
        switch (eventName) {
            case "event":
                return "task--primary";
            case "task":
                return "task--primary";
            case "meeting":
                return "task--primary";
            case "holiday":
                return "task--primary";
            case "birthdates":
                return "birthdates";
            case "anniversary":
                return "task--primary";
            case "reminder":
                return "task--primary";
            case "other":
                return "task--primary";
        }
    }
}




const itemHandler = new ItemHandler();
export default itemHandler;