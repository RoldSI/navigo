import {Component, Input} from '@angular/core';

@Component({
  selector: 'number-indicator',
  templateUrl: './number-indicator.component.html',
  styleUrls: ['./number-indicator.component.scss']
})
export class NumberIndicatorComponent {
  @Input() content: string | number = "";
  @Input() unit: string = "";
  @Input() color: string | undefined = "";
  @Input() formattingMode: string | "distance" | "time" | "co2" | "" = "";
}
