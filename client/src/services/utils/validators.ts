export const validateEmail = (e: any): boolean => {
	const re =
    /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	return !re.test(String(e.target.value).toLowerCase());
}

export const validatePassword = (e: any): boolean => {
	if (e.target.value.length >= 8) return false;
	return true
}

export const validateName = (e: any): boolean => {
	const re = /^[a-zA-Z]+$/;
	return !re.test(String(e.target.value));
}

export const validateLink = (e: any): boolean => {
	let urlPattern = new RegExp('^(https?:\\/\\/)?'+ // validate protocol
	    '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+ // validate domain name
	    '((\\d{1,3}\\.){3}\\d{1,3}))'+ // validate OR ip (v4) address
	    '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // validate port and path
	    '(\\?[;&a-z\\d%_.~+=-]*)?'+ // validate query string
	    '(\\#[-a-z\\d_]*)?$','i'); // validate fragment locator
	return !urlPattern.test(String(e.target.value));
}

export const validatePhoneNumber = (e: any): boolean => {
	if (e.target.value.match(/\b(\d{10,15})$/)) return false;
	return true;
};

export const validateTelegramLink = (e: any): boolean => {
	if (e.target.value[0] == "@") return false;
	return true;
};

export const validateSalary = (e:any): boolean=>{
	if(e.target.value>0)return false;
	return  true;
}

export const validateBirthday = (e: any): boolean=>{
	let date = new Date(e.target.value);
	let today = new Date();
	if (date.getFullYear() < today.getFullYear()){return false;}
	return true;
}

export const validateBackgroundColor = (e: any): boolean => {
	if(e.target.value[0] == "#" && isNaN(e.target.value.slice(1,-1)))return false;
	return true;
}