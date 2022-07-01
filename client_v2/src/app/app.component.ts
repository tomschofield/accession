import { Component, OnInit, ViewChild } from '@angular/core';
import { ChatService } from './chat.service';
import { GetObjectsService } from './get-objects.service';
import { NgxMasonryModule } from 'ngx-masonry';
import { NgxMasonryOptions, NgxMasonryComponent } from "ngx-masonry";
import {NgPluralizeService} from 'ng-pluralize';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  public masonryOptions: NgxMasonryOptions = {
    // gutter: 1,
    itemSelector: '.item_box',
    columnWidth: 500,
    // isAnimated: true,
  // columWidth: 270,
   gutter: 18,
   fitWidth:true
  //  transitionDuration: 0,
  //  isFitWidth: true

  };

  @ViewChild(NgxMasonryComponent) masonry: NgxMasonryComponent;  // masonry: NgxMasonryComponent;

  title = 'client_v2';
  message: string = "";
  messages: string[] = [];
  yPos: number = 0;
  scrollSpeed = 1;
  pause: boolean = false;
  accessionObjects: any[] = [];//AccessionObjects ={"objects":[]}
  collection = [];
  imgSrc: string = "assets/images/0F8A3627.JPG";
  latestMessage: any = {};
  scroll: boolean = false;
  constructor( private pluralizeService:NgPluralizeService , private objectsService: GetObjectsService) {

  }

  updateObjectStructure() {
    //todo probably remove this function
  }
  getTopCategory(item: any) {
   
    if (item.categories.length > 0) {
      console.log("singular",item.categories[0])
      console.log("plural",this.pluralizeService.pluralize(item.categories[0]))
      return this.pluralizeService.pluralize(item.categories[0]);
    }
    else {
      return "";
    }

  }
  onSubscribe() {
    console.log("this.accessionObjects ", this.accessionObjects.length);
    for (let index = 0; index < this.accessionObjects.length; index++) {
      this.accessionObjects[index]["imageSrcFocus"] = this.accessionObjects[index]['imageSrcFront0'];
    }

  }
  getClasses(object) {

    var classes = "";
    if (object['AI_keys'].length > 0) {
      if (object['AI_keys'].length ==1) {
        if (object['AI_keys'][0]['class'].length > 0) {
          if (object['AI_keys'][0]['class'][0] == "A" || object['AI_keys'][0]['class'][0] == "I" || object['AI_keys'][0]['class'][0] == "O" || object['AI_keys'][0]['class'][0] == "U") {
            classes += "n " +object['AI_keys'][0]['class'];
            return classes;
          }
          else{
            classes += " " +object['AI_keys'][0]['class'];
            return classes;
          }
        }

      }

      if (object['AI_keys'][0]['class'].length > 0) {
        if (object['AI_keys'][0]['class'][0] == "A" || object['AI_keys'][0]['class'][0] == "I" || object['AI_keys'][0]['class'][0] == "O" || object['AI_keys'][0]['class'][0] == "U") {
          classes += "n ";
        }
        else {
          classes += " ";
        }
      }
      for (let index = 0; index < object['AI_keys'].length - 1; index++) {
        classes += object['AI_keys'][index]['class'] + ", ";

      }
      classes += "or " + object['AI_keys'][object['AI_keys'].length - 1]['class'];
    }
    return classes;
  }
  changeImgSrcFocus(index, src) {
    this.accessionObjects[index]["imageSrcFocus"] = src;
    console.log("src", src);
    console.log(this.accessionObjects[index]["imageSrcFocus"]);
  }
  scrollToTop(scrollDuration: number) {
    if(scroll){
    const scrollHeight = window.scrollY,
      scrollStep = Math.PI / (scrollDuration / 15),
      cosParameter = scrollHeight / 2;
    var scrollCount = 0,
      scrollMargin,
      scrollInterval = setInterval(function () {
        if (window.scrollY != 0) {
          scrollCount = scrollCount + 1;
          scrollMargin = cosParameter - cosParameter * Math.cos(scrollCount * scrollStep);
          window.scrollTo(0, (scrollHeight - scrollMargin));
        }
        else {
          clearInterval(scrollInterval);
          window.scrollTo(0, 1000);
          console.log("scrolling to bottom");
        }

      }, 15);
    }
  }
  scrollToBottom(scrollDuration: number) {
    if(scroll){
    var body = document.body,
      html = document.documentElement;

    var height = Math.max(body.scrollHeight, body.offsetHeight,
      html.clientHeight, html.scrollHeight, html.offsetHeight);
    const scrollHeight = height,
      scrollStep = Math.PI / (scrollDuration / 15),
      cosParameter = scrollHeight / 2;
    var scrollCount = scrollHeight,
      scrollMargin,
      scrollInterval = setInterval(function () {
        if (window.scrollY < height) {
          scrollCount = scrollCount - 1;
          scrollMargin = cosParameter - cosParameter * Math.cos(scrollCount * scrollStep);
          window.scrollTo(0, (scrollHeight - scrollMargin));
        }
        else {

          window.scrollTo(0, 0);
        };
      }, 15);
    }
  }
  shuffle(a: any) {
    console.log("shuffling");
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  sendMessage() {
    // this.chatService.sendMessage(this.message);
    // this.message = '';
  }

  unixToFormatedDateTime(unixTimestamp: number) {
    var date = new Date(unixTimestamp * 1000);


    var hours = date.getHours();
    var minutes = "0" + date.getMinutes();
    var seconds = "0" + date.getSeconds();

    var formattedTime = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
    return date.toString();//.substring(0,date.toString().length-30);
  }
  testInt() {
    console.log("interval")
  }
  checkMessage() {
    var msg = this.latestMessage;
    this.messages.push(msg);
    console.log("msg", msg);
    this.pause = true;
    var body = document.body,
      html = document.documentElement;

    var height = Math.max(body.scrollHeight, body.offsetHeight,
      html.clientHeight, html.scrollHeight, html.offsetHeight);
    if (scroll) {
      window.scrollTo(0, height);
      setTimeout(() => {
        console.log("releasng pause")
        this.pause = false;
        this.yPos = window.scrollY;
      }, 4005);
    }
    console.log("adding new object to array");

    // msg['imageSrcFocus'] = msg['imageSrcFront0'];

    this.accessionObjects.push(msg);
    this.updateObjectStructure();
  }

  showConfig() {
    this.objectsService.getObjects().subscribe(
      (data: any) => this.accessionObjects = data
      , err => console.error(err), () => this.onSubscribe());

  }
  itemsLoaded() {
    console.log('itemsloaded');
  }

  ngOnInit() {
    this.showConfig();
    if (scroll) {
      setInterval(() => {
        var body = document.body,
          html = document.documentElement;

        var height = Math.max(body.scrollHeight, body.offsetHeight,
          html.clientHeight, html.scrollHeight, html.offsetHeight);
        if (!this.pause) {
          window.scrollTo(0, this.yPos);
          this.yPos += this.scrollSpeed;
          if (this.yPos >= height || this.yPos <= 0) {
            this.scrollSpeed *= -1;
          }
        }
      }, 15);
    }


    //  this.chatService.getMessages().subscribe(
    //   (data: any) => this.latestMessage = data
    //   , err => console.error(err), () => this.checkMessage());


    // this.chatService
    //   .getMessages()
    //   .subscribe(message => {
    //     console.log("message", message);
    //     this.latestMessage = message;
    //     // this.messages.push(message);
    //     this.checkMessage()
    //   });


  }
  
}
export interface AccessionObjects {
  objects: any[];
}
