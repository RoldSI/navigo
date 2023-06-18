import {Component} from '@angular/core';
import {AuthService} from "../utils/auth.service";
import {ApiService} from '../utils/api.service';
import {ColormapService} from "../utils/color.service";
import {MapRoutingService} from "../utils/map-routing.service";

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {
  loggedIn = false;
  userEf: number = -1;
  efficiencyColor: string = "#000000";

  data: any[] = []
  visible: boolean = false;

  showDialog(): void {
    this.visible = true;
  }

  generateTableData() {
    this.data = [];
    for (let i = 1; i <= 20; i++) {
      const entry = {
        ranking: i,
        efficiencyScore: Math.floor(Math.random() * 100),
        username: `User ${i}`
      };
      this.data.push(entry);
    }
    this.data.sort((a, b) => b.efficiencyScore - a.efficiencyScore);
  }

  constructor(private authService: AuthService,
              private apiService: ApiService,
              private colorService: ColormapService,
              private mapRoutingService: MapRoutingService) {
    this.generateTableData();

    this.authService.loggedIn$.subscribe((loggedIn) => {
      this.loggedIn = loggedIn;
    });
    this.mapRoutingService.updateEfficiencyScore$.subscribe((something) => {
      this.updateUserEff();
    })
    this.updateUserEff();
  }

  login(): void {
    this.authService.login();
  }

  logout(): void {
    this.authService.logout();
  }

  public updateUserEff() {
    this.apiService.getUserEfficiency().subscribe((res) => {
      this.userEf = res['score'];
      this.efficiencyColor = this.colorService.getColor(this.userEf, 0, 100);
    });
  }
}
