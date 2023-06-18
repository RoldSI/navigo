import {Injectable} from "@angular/core";
import {HttpErrorResponse, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from "@angular/common/http";
import {AuthService} from "./auth.service";
import {catchError, Observable, throwError} from "rxjs";
import {MessageService} from "primeng/api";

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


@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
  constructor(private messageService: MessageService) {
  }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(request)
      .pipe(
        catchError((error: HttpErrorResponse) => {
          let errorMessage = 'An error occurred';
          if (error.error instanceof ErrorEvent) {
            // Client-side error
            errorMessage = `Error: ${error.error.message}`;
          } else {
            // Server-side error
            errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
          }
          this.messageService.add({severity: 'error', summary: 'Error', detail: errorMessage});

          return throwError(errorMessage);
        })
      )
  }
}
