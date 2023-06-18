import {Component, Input} from '@angular/core';
import {MapRoutingService, RouteDirectionResult} from '../utils/map-routing.service';
import {ApiService} from '../utils/api.service';

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
  @Input() routeEval: RouteDirectionResult | undefined;

  addRoute() {
    if (!this.routeEval) return;
    // this.routeEval.time
    // this.routeEval?.catastrophy,
    alert("implement...");
    // this.apiService.addRouteToUser(this.routeEval.efficiency,
    //   this.routeEval.distance,
    //   0,
    //   'from',
    //   'to',
    //   0,
    //   'something');
  }
}
