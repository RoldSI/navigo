import {Injectable} from "@angular/core";
import {Observable} from "rxjs";
import {environment} from "../../environments/environment";
import {HttpClient, HttpEvent, HttpHandler, HttpHeaders, HttpInterceptor, HttpRequest} from "@angular/common/http";
import {AuthService} from './auth.service';

export type InputObject = {
  input: string[];
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private token: string = "";

  constructor(private http: HttpClient) {
  }

  private addTokenToHeaders(headers: HttpHeaders): HttpHeaders {
    if (this.token) {
      return headers.set('Authorization', `Bearer ${this.token}`);
    }
    return headers;
  }

  private getRequestOptions(): { headers: HttpHeaders } {
    let headers = new HttpHeaders();
    headers = this.addTokenToHeaders(headers);
    return {headers: headers};
  }

  addFavorite(input: InputObject): Observable<any> {
    const options = this.getRequestOptions();
    return this.http.post<any>(`${environment.apiBase}/favorites`, input, options);
  }

  removeFavorite(input: InputObject): Observable<any> {
    const options = this.getRequestOptions();
    return this.http.delete<any>(`${environment.apiBase}/favorites`, {body: input, ...options});
  }

  getFavorites(): Observable<any> {
    const options = this.getRequestOptions();
    return this.http.get<any>(`${environment.apiBase}/favorites`, options);
  }

  generateChatGPTSuggestion(input: InputObject): Observable<any> {
    const options = this.getRequestOptions();
    return this.http.get<any>(`${environment.apiBase}/suggestions`, {params: input, ...options});
  }

  getRoutes(): Observable<any> {
    const options = this.getRequestOptions();
    return this.http.get<any>(`${environment.apiBase}/routes`, options);
  }

  authenticateDemo(): Observable<any> {
    const options = this.getRequestOptions();
    return this.http.get<any>(`${environment.apiBase}/authenticateDemo`, options);
  }

  public setToken(token: string | undefined): void {
    this.token = token || '';
  }
}
