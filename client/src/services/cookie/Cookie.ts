class Cookie {
	storage: string;
	constructor() {
		this.storage = document.cookie;
	}
	get(key: string) {
		return this.storage.split(";").filter((item) => {
			return item === key;
		})[0].split("=")[1];

	}

	set(key: string, value: string, expiresMonth: number) {
		const date = new Date();
		date.setMonth(date.getMonth() + expiresMonth);
		document.cookie = key + "=" + value + ";expires=" + date.toUTCString();
	}
	remove(key: string) {
		return this.storage.split(";").filter((item) => {
			return item !== key;
		}).join(";");
	}
}

export default new Cookie();
