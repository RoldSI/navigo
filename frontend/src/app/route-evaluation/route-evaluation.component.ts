import {Component, Input} from '@angular/core';

export type RouteEvaluation = {
  name: string,
  co2: number,
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

}
