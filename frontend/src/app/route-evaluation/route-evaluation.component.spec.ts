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
});
