import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';
import {GoogleMapsModule} from '@angular/google-maps';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {MapComponentComponent} from './map-component/map-component.component';
import {SidebarComponent} from './sidebar/sidebar.component';
import {ButtonModule} from "primeng/button";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {RippleModule} from "primeng/ripple";
import { HeaderComponent } from './header/header.component';

@NgModule({
  declarations: [
    AppComponent,
    MapComponentComponent,
    SidebarComponent,
    HeaderComponent
  ],
  imports: [
    BrowserModule,
    GoogleMapsModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    ButtonModule,
    RippleModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
