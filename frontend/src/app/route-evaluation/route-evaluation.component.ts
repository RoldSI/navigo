import {Component, Input} from '@angular/core';
import {MapRoutingService, RouteDirectionResult} from '../utils/map-routing.service';
import {ApiService} from "../utils/api.service";
import {MessageService} from "primeng/api";

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
  private _routeEval: RouteDirectionResult | undefined;

  constructor(private mapRoutingService: MapRoutingService,
              private apiService: ApiService,
              private messageService: MessageService) {
  }

  @Input() routeEval: RouteDirectionResult | undefined;

  @Input() colorMap: Map<string, string> | undefined;

  getColor(key: string): string {
    return this.colorMap?.get(key) || ""
  }

  private savingSuccessfull() {
    this.messageService.add({
      severity: 'success',
      summary: 'Route successfully added.',
      detail: 'You have successfully added the route to your taken routes. It will be considered in your efficiency score.'
    });
  }

  addRoute() {
    if (!this.routeEval) return;
    this.apiService.addRouteToUser(this.routeEval.efficiency,
      this.routeEval.distance,
      this.routeEval.duration,
      this.mapRoutingService.startLocation,
      this.mapRoutingService.endLocation,
      this.routeEval.catastrophy,
      this.routeEval.mode).subscribe((res) => {
      this.mapRoutingService.updateEfficiencyScore();
      this.savingSuccessfull();
    })
  }
}
