import {Injectable} from "@angular/core";
import {HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from "@angular/common/http";
import {AuthService} from "./auth.service";
import {Observable} from "rxjs";

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private authService: AuthService) {
  }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    if (!this.authService.getToken()) {
      console.warn("No token!");
    }
    req = req.clone({
      setHeaders: {
        "Content-Type": 'application/json',
        "Authorization": `${this.authService.getToken()}`,
      },
    });

    return next.handle(req);
  }
}
