import {Component} from '@angular/core';
import {MapRoutingService, RouteDirectionResult} from "../utils/map-routing.service";
import {Observable} from "rxjs";

@Component({
  selector: 'mode-overview',
  templateUrl: './mode-overview.component.html',
  styleUrls: ['./mode-overview.component.scss']
})
export class ModeOverviewComponent {
  loading: boolean = false;

  routes: Observable<RouteDirectionResult[]> = new Observable<RouteDirectionResult[]>();

  constructor(private readonly mapRoutingService: MapRoutingService) {
    this.mapRoutingService.routesLoading$.subscribe((b) => this.loading = b);
    this.routes = this.mapRoutingService.route$;
  }
}
