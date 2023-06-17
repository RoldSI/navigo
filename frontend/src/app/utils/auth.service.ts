import {inject, Injectable} from "@angular/core";
import {Auth, GoogleAuthProvider, signInWithPopup} from "@angular/fire/auth";
import {ApiService} from "./api.service";
import {signOut} from "@firebase/auth";
import {CookieService} from "ngx-cookie-service";
import {BehaviorSubject} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private auth: Auth = inject(Auth);
  provider: GoogleAuthProvider = new GoogleAuthProvider();
  private authTokenCookieName = 'authToken';
  private authToken: string | undefined;

  public loggedIn$: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);

  constructor(private apiService: ApiService, private cookieService: CookieService) {
    // Check if the authentication token exists in the cookie on initialization
    this.authToken = this.getAuthTokenFromCookie();
    if (this.authToken) {
      this.loggedIn$.next(true);
    }
  }

  getToken(): string | undefined {
    return this.authToken;
  }

  logout(): void {
    this.loggedIn$.next(false);
    this.cookieService.delete(this.authTokenCookieName);
    signOut(this.auth);
  }

  login(): void {
    signInWithPopup(this.auth, this.provider)
      .then((result) => {
        // This gives you a Google Access Token. You can use it to access the Google API.
        const credential = GoogleAuthProvider.credentialFromResult(result);
        // Set Token
        this.authToken = credential?.accessToken;
        this.setAuthTokenInCookie(this.authToken);
        // The signed-in user info.
        const user = result.user;
        this.loggedIn$.next(true);
        console.log(user);
      }).catch((error) => {
      // Handle Errors here.
      const errorCode = error.code;
      const errorMessage = error.message;
      // The email of the user's account used.
      const email = error.customData.email;
      // The AuthCredential type that was used.
      const credential = GoogleAuthProvider.credentialFromError(error);
      this.loggedIn$.next(false);
    })
  }

  private setAuthTokenInCookie(authToken: string | undefined): void {
    if (authToken) {
      this.cookieService.set(this.authTokenCookieName, authToken, 30, '/');
    }
  }

  private getAuthTokenFromCookie(): string | undefined {
    return this.cookieService.get(this.authTokenCookieName);
  }
}
