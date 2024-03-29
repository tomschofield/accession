import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NgxMasonryModule } from 'ngx-masonry';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { NgPluralizeModule } from 'ng-pluralize';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgxMasonryModule,
    HttpClientModule,
    BrowserAnimationsModule,
    NgPluralizeModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
