import {Component, Input} from '@angular/core';
import {MapRoutingService} from '../utils/map-routing.service';
import {ApiService} from '../utils/api.service';
import {HeaderComponent} from '../header/header.component';

export type RouteEvaluation = {
  name: string,
  co2: number,
  efficiency: number,
  catastrophy: number,
  distance: number,
  time: number
}

@Component({
  selector: 'route-evaluation',
  templateUrl: './route-evaluation.component.html',
  styleUrls: ['./route-evaluation.component.scss']
})
export class RouteEvaluationComponent {
  @Input() routeEval: RouteEvaluation | undefined;

  constructor(private mapRoutingService: MapRoutingService, private apiService: ApiService) {

    // TODO: Später
    // this.loadSuggestions("Karlsruhe")
  }

  addRoute() {
    this.apiService.addRouteToUser(<number>this.routeEval?.efficiency, <number>this.routeEval?.distance, <number>this.routeEval?.time, 'from', 'to', <number>this.routeEval?.catastrophy, 'something').subscribe((res) => {
      
    });
  }

}
