class Cookie {
	storage: string;
	constructor() {
		this.storage = document.cookie;
	}
	// to check if cookie exists
	isFound(key: string) {
		return this.storage.indexOf(key) !== -1;
	}
	// get cookie value by key name
	get(key: string) {
		if (this.isFound(key)) {
			return this.storage.split(";").filter((item) => {
				return item.indexOf(key) !== -1;
			}).join(";");
		}
		else {
			throw new Error("Cookie not found to be retrieved");
		}
	}
	// to set cookie value
	set(key: string, value: string, expiresMonth: number) {
		if (!this.isFound(key)) {
			const date = new Date();
			date.setMonth(date.getMonth() + expiresMonth);
			document.cookie = `${key}=${value};expires=${date.toUTCString()}`;
		}
		else {
			throw new Error("Cookie already exists");
		}
	}

	// update cookie value
	update(key: string, value: string, expiresMonth: number) {
		if (this.isFound(key)) {
			this.remove(key);
			this.set(key, value, expiresMonth);
		}
		else {
			throw new Error("Cookie not found to be updated");
		}
	}
	// to remove cookie value
	remove(key: string) {
		if (this.isFound(key)) {
			return this.storage.split(";").filter((item) => {
				return item !== key;
			}).join(";");
		}
		else {
			throw new Error("Cookie not found to be removed");
		}
	}

}

export default new Cookie();
