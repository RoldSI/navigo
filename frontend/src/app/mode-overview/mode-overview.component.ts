import { Component } from '@angular/core';
import { RouteEvaluation } from '../route-evaluation/route-evaluation.component';

@Component({
  selector: 'mode-overview',
  templateUrl: './mode-overview.component.html',
  styleUrls: ['./mode-overview.component.scss'],
})
export class ModeOverviewComponent {
  routes: RouteEvaluation[] = [
    {
      name: 'Route 1',
      co2: 123,
      distance: 321,
      time: 1,
      efficiency: 98,
      catastrophy: 1,
    },
    {
      name: 'Route 2',
      co2: 999,
      distance: 321,
      time: 1,
      efficiency: 98,
      catastrophy: 76,
    },
    {
      name: 'Route 1',
      co2: 123,
      distance: 321,
      time: 1,
      efficiency: 98,
      catastrophy: 74,
    },
    {
      name: 'Route 2',
      co2: 999,
      distance: 321,
      time: 1,
      efficiency: 98,
      catastrophy: 75,
    },
    {
      name: 'Route 1',
      co2: 123,
      distance: 321,
      time: 1,
      efficiency: 98,
      catastrophy: 40,
    },
    {
      name: 'Route 2',
      co2: 999,
      distance: 321,
      time: 1,
      efficiency: 98,
      catastrophy: 99,
    },
  ];
}
