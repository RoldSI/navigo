import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';
import {GoogleMapsModule} from '@angular/google-maps';

import {initializeApp, provideFirebaseApp} from '@angular/fire/app';
import {getAuth, provideAuth} from '@angular/fire/auth';

import {DialogModule} from 'primeng/dialog';
import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {MapComponentComponent} from './map-component/map-component.component';
import {SidebarComponent} from './sidebar/sidebar.component';
import {ButtonModule} from "primeng/button";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {RippleModule} from "primeng/ripple";
import {environment} from '../environments/environment';
import {HeaderComponent} from './header/header.component';
import {ModeOverviewComponent} from './mode-overview/mode-overview.component';
import {RouteEvaluationComponent} from './route-evaluation/route-evaluation.component';
import {NumberIndicatorComponent} from './number-indicator/number-indicator.component';
import {HTTP_INTERCEPTORS, HttpClientModule} from "@angular/common/http";
import {AuthService} from "./utils/auth.service";
import {ApiService} from "./utils/api.service";
import {AuthInterceptor, ErrorInterceptor} from "./utils/auth.interceptor";
import {AutoCompleteModule} from "primeng/autocomplete";
import {FormsModule} from "@angular/forms";
import {TooltipModule} from 'primeng/tooltip';
import {ProgressSpinnerModule} from 'primeng/progressspinner';
import {ColormapService} from "./utils/color.service";
import {
  Co2Pipe,
  Co2UnitPipe,
  DistanceFormatPipe,
  DistanceUnitPipe,
  RoundToTwoDecimalsPipe,
  TimeFormatPipe,
  TimeUnitPipe
} from "./utils/formatting.pipes";
import {ToastModule} from "primeng/toast";
import {MessageService} from "primeng/api";
import {TableModule} from "primeng/table";
import {InputTextModule} from "primeng/inputtext";

@NgModule({
  declarations: [
    AppComponent,
    MapComponentComponent,
    SidebarComponent,
    HeaderComponent,
    ModeOverviewComponent,
    RouteEvaluationComponent,
    NumberIndicatorComponent,
    DistanceFormatPipe,
    TimeFormatPipe,
    DistanceUnitPipe,
    TimeUnitPipe,
    RoundToTwoDecimalsPipe, Co2UnitPipe,
    Co2Pipe
  ],
  imports: [
    TooltipModule,
    ProgressSpinnerModule,
    ToastModule,
    BrowserModule,
    GoogleMapsModule,
    FormsModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    DialogModule,
    TableModule,
    InputTextModule,
    ButtonModule,
    HttpClientModule,
    RippleModule,
    provideFirebaseApp(() => initializeApp(environment.firebaseConfig)),
    provideAuth(() => getAuth()),
    AutoCompleteModule,
  ],
  providers: [
    AuthService,
    ApiService,
    ColormapService,
    MessageService,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true,
    },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: ErrorInterceptor,
      multi: true
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
