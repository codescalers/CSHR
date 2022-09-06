class LocalStorage {
    storage: Storage;
    constructor() {
        this.storage = window.localStorage;
    }
    get(key: string) {
        return this.storage.getItem(key);
    }
    set(key: string, value: string) {
        this.storage.setItem(key, value);
    }
    remove(key: string) {
        this.storage.removeItem(key);
    }
}


export default new LocalStorage();