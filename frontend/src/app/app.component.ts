import {Component} from '@angular/core';
import {ApiService} from "./utils/api.service";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'frontend';

  constructor(private apiService: ApiService) {
    // Example of Adding and Reading Favorites...
    this.apiService.addFavorite({input: ["New Fav"]}).subscribe((res) => {
      console.log(res);

      this.apiService.getFavorites().subscribe((res) => {
        console.log(res);
      });
    })
  }
}
