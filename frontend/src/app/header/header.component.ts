import {Component} from '@angular/core';
import {AuthService} from "../utils/auth.service";
import {ApiService} from '../utils/api.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {
  loggedIn = false;
  userEf : number = -1;

  constructor(private authService: AuthService, private apiService: ApiService) {
    this.authService.loggedIn$.subscribe((loggedIn) => {
      this.loggedIn = loggedIn;
    });
    this.userEff();
  }

  login(): void {
    this.authService.login();
  }

  logout(): void {
    this.authService.logout();
  }

  public userEff() {
    this.apiService.getUserEfficiency().subscribe((res) => {
      this.userEf = res['score'];
    });
  }
}
