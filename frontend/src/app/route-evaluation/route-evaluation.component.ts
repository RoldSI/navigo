import { Component, Input } from '@angular/core';
import { MapRoutingService } from '../utils/map-routing.service';
import { ApiService } from '../utils/api.service';

export type RouteEvaluation = {
  name: string;
  co2: number;
  efficiency: number;
  catastrophy: number;
  distance: number;
  time: number;
};

@Component({
  selector: 'route-evaluation',
  templateUrl: './route-evaluation.component.html',
  styleUrls: ['./route-evaluation.component.scss'],
})
export class RouteEvaluationComponent {
  @Input() routeEval: RouteEvaluation | undefined;
  highCatastrophy: boolean = false; // Variable to track high catastrophe score

  ngOnChanges() {
    if (this.routeEval && this.routeEval.catastrophy > 75) {
      this.highCatastrophy = true; // Set the variable to true if catastrophe score is high
    } else {
      this.highCatastrophy = false; // Set the variable to false if not
    }
  }
  constructor(
    private mapRoutingService: MapRoutingService,
    private apiService: ApiService
  ) {
    // TODO: Später
    // this.loadSuggestions("Karlsruhe")
  }

  addRoute() {
    this.apiService.addRouteToUser(
      <number>this.routeEval?.efficiency,
      <number>this.routeEval?.distance,
      <number>this.routeEval?.time,
      'from',
      'to',
      <number>this.routeEval?.catastrophy,
      'something'
    );
  }
}
