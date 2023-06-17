import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';
import {GoogleMapsModule} from '@angular/google-maps';

import {initializeApp, provideFirebaseApp} from '@angular/fire/app';
import {getAuth, provideAuth} from '@angular/fire/auth';

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
import {AuthInterceptor} from "./utils/auth.interceptor";

@NgModule({
  declarations: [
    AppComponent,
    MapComponentComponent,
    SidebarComponent,
    HeaderComponent,
    ModeOverviewComponent,
    RouteEvaluationComponent,
    NumberIndicatorComponent
  ],
  imports: [
    BrowserModule,
    GoogleMapsModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    ButtonModule,
    HttpClientModule,
    RippleModule,
    provideFirebaseApp(() => initializeApp(environment.firebaseConfig)),
    provideAuth(() => getAuth()),
  ],
  providers: [
    AuthService,
    ApiService,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true,
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
