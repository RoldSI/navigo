import {Component} from '@angular/core';
import {ApiService} from "../utils/api.service";


@Component({
  selector: 'sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent {
  suggestions: { address: string, location: string }[] = [];

  constructor(private apiService: ApiService) {
    this.loadSuggestions("Karlsruhe")
  }

  loadSuggestions(addr: string): void {
    this.apiService.generateChatGPTSuggestion({input: addr}).subscribe((res) => {
      const cleanedJsonString = res.places.replace(/\\n/g, '');
      const jsonObject = JSON.parse(cleanedJsonString);

      this.suggestions = Object.keys(jsonObject).map(key => {
        return jsonObject[key];
      });

      // TODO: Emit the "address" to the Map to draw the suggestions
    })
  }
}
