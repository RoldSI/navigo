import { Component, Input } from '@angular/core';
import { RouteDirectionResult } from '../utils/map-routing.service';
import { ColormapService } from '../utils/color.service';

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
  constructor(private colorService: ColormapService) {}

  @Input() routeEval: RouteDirectionResult | undefined;

  @Input() colorMap: Map<string, string> | undefined;

  getColor(key: string): string {
    return this.colorMap?.get(key) || '';
  }

  addRoute() {
    if (!this.routeEval) return;
    // this.routeEval.time
    // this.routeEval?.catastrophy,
    alert('implement...');
    // this.apiService.addRouteToUser(this.routeEval.efficiency,
    //   this.routeEval.distance,
    //   0,
    //   'from',
    //   'to',
    //   0,
    //   'something');
  }

  highCatastrophy: boolean = false; // Variable to track high catastrophe score

  ngOnChanges() {
    if (this.routeEval && this.routeEval.catastrophy > 75) {
      this.highCatastrophy = true; // Set the variable to true if catastrophe score is high
    } else {
      this.highCatastrophy = false; // Set the variable to false if not
    }
  }
}
