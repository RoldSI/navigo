import { Component, Input, Renderer2, ElementRef } from '@angular/core';

export type RouteEvaluation = {
  name: string;
  co2: number;
  distance: number;
  time: number;
  catastrophy: number;
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
}
