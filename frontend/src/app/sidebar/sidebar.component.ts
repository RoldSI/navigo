import {Component} from '@angular/core';
import {ApiService} from "../utils/api.service";
import {AutoCompleteCompleteEvent} from "primeng/autocomplete";
import {MapRoutingService} from "../utils/map-routing.service";

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
  destinationMode: SEARCH_MODE = SEARCH_MODE.DESTINATION;
  start: any;
  destination: any;
  startSuggestions: string[] = [];
  destinationSuggestions: string[] = [];

  public search(mode: SEARCH_MODE, event: AutoCompleteCompleteEvent): void {
    const queryString = event.query;
    this.apiService.getAutocompleteSuggestions({input: queryString}).subscribe((res) => {
      if (mode === SEARCH_MODE.START) {
        this.startSuggestions = res;
      } else if (mode == SEARCH_MODE.DESTINATION) {
        this.destinationSuggestions = res;
      }
    })
  }

  suggestions: { address: string, location: string }[] = [];
  introText: string | undefined;

  constructor(private mapRoutingService: MapRoutingService, private apiService: ApiService) {
    this.loadInitialHelpText();
    this.mapRoutingService.suggestions$.subscribe((s) => {
      this.suggestions = s;
    })
    // TODO: Später
    // this.loadSuggestions("Karlsruhe")
  }

  startSearch(): void {
    this.mapRoutingService.createDirectionRequest(this.start, this.destination);
  }

  loadInitialHelpText(): void {
    this.apiService.generateChatGPTIntro().subscribe((res: any) => {
      this.introText = res.intro;
    })
  }
}
