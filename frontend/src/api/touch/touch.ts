import { BaseApi } from '../BaseApi';

export interface TouchResponse {
	id: string;
	count?: string;
}

class TouchMeApi extends BaseApi {
	constructor() {
		super('', import.meta.env.VITE_API_BASE_URL ?? document.location.origin);
	}
	public async getTouch() {
		return this.get<TouchResponse>('/touch');
	}
	public async addTouch() {
		return this.post<TouchResponse>('/touch');
	}
}

export const touchMeApi = new TouchMeApi();
