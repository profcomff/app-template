import axios, { AxiosResponse } from 'axios';
import queryString from 'query-string';

export interface DefaultResponse {
	status: string;
	message: string;
}

type Path = `/${string}` | '';

export class BaseApi {
	url: string;

	constructor(path: Path) {
		this.url = import.meta.env.VITE_API_URL + path;
	}

	protected async get<Response, Params = never>(
		path: Path,
		params?: Partial<Params>,
		headers: Record<string, string> = {},
	): Promise<AxiosResponse<Response>> {
		return axios.get<Response>(`${this.url}${path}`, {
			params,
			headers,
			paramsSerializer: {
				serialize: params => queryString.stringify(params, { arrayFormat: 'none' }),
			},
		});
	}

	protected async post<Response, Body = never, Params = never>(
		path: Path,
		body?: Body,
		params?: Params,
		headers: Record<string, string> = {},
	): Promise<AxiosResponse<Response>> {
		return axios.post<Response, AxiosResponse<Response>, Body>(`${this.url}${path}`, body, { headers, params });
	}

	protected async delete<Response = never, Params = never>(
		path: Path,
		params?: Params,
		headers: Record<string, string> = {},
	): Promise<AxiosResponse<Response>> {
		return axios.delete<Response>(`${this.url}${path}`, { params, headers });
	}

	protected async patch<Response = never, Body = never>(
		path: Path,
		body?: Body,
		headers: Record<string, string> = {},
	): Promise<AxiosResponse<Response>> {
		return axios.patch<Response, AxiosResponse<Response>, Body>(`${this.url}${path}`, body, { headers });
	}

	protected async put<Response = never, Body = never, Params = never>(
		path: Path,
		body?: Body,
		params?: Params,
	): Promise<AxiosResponse<Response>> {
		return axios.put(`${this.url}${path}`, body, { params });
	}
}
