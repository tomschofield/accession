import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { HttpClientModule } from '@angular/common/http';
import { AppComponent } from './app.component';
import { ChatService } from 'chat.service';
import { GetObjectsService } from './get-objects.service';

//import { NgxMasonryModule } from 'ngx-masonry';
import { MasonryModule } from 'angular2-masonry';


@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    HttpModule,
    MasonryModule
  ],
  providers: [ChatService,GetObjectsService],
  bootstrap: [AppComponent]
})
export class AppModule { }
