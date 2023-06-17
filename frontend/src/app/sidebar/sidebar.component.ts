import {Component} from '@angular/core';
import {ApiService} from "../utils/api.service";
import {AutoCompleteCompleteEvent} from "primeng/autocomplete";

enum SEARCH_MODE {
  START,
  DESTINATION
}

@Component({
  selector: 'sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent {
  startMode: SEARCH_MODE = SEARCH_MODE.START;
  destinationMode: SEARCH_MODE = SEARCH_MODE.START;
  start: any;
  destination: any;
  startSuggestions: string[] = [];
  destinationSuggestions: string[] = [];

  public search(mode: SEARCH_MODE, event: AutoCompleteCompleteEvent): void {
    console.log(mode, event);
    const queryString = event.query;
    if (mode === SEARCH_MODE.START) {

    } else if (mode == SEARCH_MODE.DESTINATION) {

    }
    // this.suggestions = [...Array(10).keys()].map(item => event.query + '-' + item);
  }

  suggestions: { address: string, location: string }[] = [];
  introText: string | undefined;

  constructor(private apiService: ApiService) {
    this.loadInitialHelpText();
    // TODO: Später
    // this.loadSuggestions("Karlsruhe")
  }

  startSearch(): void {
    this.apiService.getRoutes({from: "Karlsruhe HBF", to: "Durlach Bahnhof"}).subscribe((res) => {
      console.log(res);
    })
  }

  loadInitialHelpText(): void {
    this.apiService.generateChatGPTIntro().subscribe((res) => {
      this.introText = res.intro;
    })
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
