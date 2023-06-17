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

  generateChatGPTIntro(): Observable<any> {
    return this.http.get<any>(`${environment.apiBase}/intro`);
  }

  getRoutes(sourceDestination: { from: string, to: string }): Observable<any> {
    // const options = this.getRequestOptions();
    return this.http.get<any>(`${environment.apiBase}/routes`, {params: sourceDestination});
  }

  authenticateDemo(): Observable<any> {
    // const options = this.getRequestOptions();
    return this.http.get<any>(`${environment.apiBase}/authenticateDemo`);
  }

  addRouteToUser( efficiency : number, distance : number, duration: number, from: string, to: string, catastrophy: number, mode: string ) {
    const currentDateTime = new Date();
    const year = currentDateTime.getFullYear();
    const month = String(currentDateTime.getMonth() + 1).padStart(2, '0'); // Adding 1 to month since it's zero-based
    const day = String(currentDateTime.getDate()).padStart(2, '0');
    const hours = String(currentDateTime.getHours()).padStart(2, '0');
    const minutes = String(currentDateTime.getMinutes()).padStart(2, '0');
    const seconds = String(currentDateTime.getSeconds()).padStart(2, '0');
    const milliseconds = String(currentDateTime.getMilliseconds()).padStart(3, '0');
    const formattedDateTime = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}.${milliseconds}`;

    return this.http.post<any>(`${environment.apiBase}/user/routes`, {
      "from" : from,
      "to": to,
      "duration": duration,
      "distance": distance,
      "efficiency": efficiency,
      "catastrophy": catastrophy,
      "datetime": formattedDateTime,
      "mode": mode
    });
  }

  public setToken(token: string | undefined): void {
    this.token = token || '';
  }
}
