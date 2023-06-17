import {Injectable} from "@angular/core";
import {Observable} from "rxjs";
import {environment} from "../../environments/environment";
import {HttpClient} from "@angular/common/http";

export type InputObjectStringList = {
  input: string[];
}

export type InputObjectString = {
  input: string;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private token: string = "";

  constructor(private http: HttpClient) {
  }

  addFavorite(input: InputObjectStringList): Observable<any> {
    // const options = this.getRequestOptions();
    console.log("add favorite: ", input);
    return this.http.post<any>(`${environment.apiBase}/favorites`, input);
  }

  removeFavorite(input: InputObjectStringList): Observable<any> {
    return this.http.delete<any>(`${environment.apiBase}/favorites`, {body: input});
  }

  getFavorites(): Observable<any> {
    console.log("get favorites");
    return this.http.get<any>(`${environment.apiBase}/favorites`);
  }

  generateChatGPTSuggestion(input: InputObjectString): Observable<any> {
    return this.http.get<any>(`${environment.apiBase}/suggestions`, {params: input});
  }

  generateChatGPTIntro(input: InputObjectString): Observable<any> {
    return this.http.get<any>(`${environment.apiBase}/intro`);
  }

  getRoutes(): Observable<any> {
    // const options = this.getRequestOptions();
    return this.http.get<any>(`${environment.apiBase}/routes`);
  }

  authenticateDemo(): Observable<any> {
    // const options = this.getRequestOptions();
    return this.http.get<any>(`${environment.apiBase}/authenticateDemo`);
  }

  public setToken(token: string | undefined): void {
    this.token = token || '';
  }
}
