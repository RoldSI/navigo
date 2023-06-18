import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RouteEvaluationComponent } from './route-evaluation.component';

describe('RouteEvaluationComponent', () => {
  let component: RouteEvaluationComponent;
  let fixture: ComponentFixture<RouteEvaluationComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [RouteEvaluationComponent]
    });
    fixture = TestBed.createComponent(RouteEvaluationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
  highCatastrophy: boolean = false; // Variable to track high catastrophe score

  ngOnChanges() {
    if (this.routeEval && this.routeEval.catastrophy > 75) {
      this.highCatastrophy = true; // Set the variable to true if catastrophe score is high
    } else {
      this.highCatastrophy = false; // Set the variable to false if not
    }
  }
});
