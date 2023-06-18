import {Component} from '@angular/core';
import {MapRoutingService, RouteDirectionResult} from "../utils/map-routing.service";
import {Observable} from "rxjs";
import {ColormapService} from "../utils/color.service";

@Component({
  selector: 'mode-overview',
  templateUrl: './mode-overview.component.html',
  styleUrls: ['./mode-overview.component.scss'],
})
export class ModeOverviewComponent {
  loading: boolean = false;
  colorMap: Map<string, string>[] = [];

  routes: RouteDirectionResult[] = [];

  constructor(private readonly mapRoutingService: MapRoutingService, private readonly colorMapService: ColormapService) {
    this.mapRoutingService.routesLoading$.subscribe((b) => this.loading = b);

    this.mapRoutingService.route$.subscribe((r)=> {
      this.colorMap = this.colorMapService.generateColormap(r);
      this.routes = r;
    })
  }
}
