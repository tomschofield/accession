import { Component, OnInit, ViewChild } from '@angular/core';
import { ChatService } from './chat.service';
import { GetObjectsService } from './get-objects.service';
import { NgxMasonryModule } from 'ngx-masonry';
import { NgxMasonryOptions, NgxMasonryComponent } from "ngx-masonry";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  public masonryOptions: NgxMasonryOptions = {
    gutter: 50 ,
     itemSelector: '.item_box',
    columnWidth: 500,
    
  };

  @ViewChild(NgxMasonryComponent) masonry: NgxMasonryComponent;  // masonry: NgxMasonryComponent;
  
  title = 'client_v2';
  message: string ="";
  messages: string[] = [];
  yPos: number = 0;
  scrollSpeed = 1;
  pause: boolean = false;
  accessionObjects: any [] = [];//AccessionObjects ={"objects":[]}
  collection = [];
  imgSrc: string = "assets/images/0F8A3627.JPG";
  latestMessage: any = {};
  constructor(private chatService: ChatService, private objectsService: GetObjectsService) {

  }

  updateObjectStructure(){
    //todo probably remove this function
  }
  getTopCategory(item:any){
   
    if(item.categories.length>0){
      return item.categories[0];
    }
    else{
      return "";
    }
    
  }
  onSubscribe(){
    console.log("this.accessionObjects ",this.accessionObjects.length );
    for (let index = 0; index < this.accessionObjects.length; index++) {
      this.accessionObjects[index]["imageSrcFocus"]=this.accessionObjects[index]['imageSrcFront0'];
    }
    
}
getClasses(object){
 
  var classes = "";
  if(object['AI_keys'].length>0){
    
    if(object['AI_keys'][0]['class'].length>0){
      if(object['AI_keys'][0]['class'][0]=="A" || object['AI_keys'][0]['class'][0]=="I" || object['AI_keys'][0]['class'][0]=="O" || object['AI_keys'][0]['class'][0]=="U" ){
        classes+="n ";
      } 
      else{
        classes+=" ";
      }
    }
    for (let index = 0; index < object['AI_keys'].length-1; index++) {
      classes += object['AI_keys'][index]['class']+", ";
      
    }
    classes += "or "+object['AI_keys'][object['AI_keys'].length-1]['class'];
  }
  return classes;
}
changeImgSrcFocus(index,src){
  this.accessionObjects[index]["imageSrcFocus"]=src;
  console.log("src",src);
}
scrollToTop(scrollDuration: number) {

  const   scrollHeight = window.scrollY,
  scrollStep = Math.PI / ( scrollDuration / 15 ),
  cosParameter = scrollHeight / 2;
  var     scrollCount = 0,
  scrollMargin,
  scrollInterval = setInterval( function() {
    if ( window.scrollY != 0 ) {
      scrollCount = scrollCount + 1;  
      scrollMargin = cosParameter - cosParameter * Math.cos( scrollCount * scrollStep );
      window.scrollTo( 0, ( scrollHeight - scrollMargin ) );
    } 
    else {
      clearInterval(scrollInterval); 
      window.scrollTo( 0,1000);
      console.log("scrolling to bottom");
    }

  }, 15 );
}
scrollToBottom(scrollDuration: number) {
  var body = document.body,
  html = document.documentElement;

  var height = Math.max( body.scrollHeight, body.offsetHeight, 
   html.clientHeight, html.scrollHeight, html.offsetHeight );
  const   scrollHeight = height,
  scrollStep = Math.PI / ( scrollDuration / 15 ),
  cosParameter = scrollHeight / 2;
  var     scrollCount = scrollHeight,
  scrollMargin,
  scrollInterval = setInterval( function() {
    if ( window.scrollY < height ) {
      scrollCount = scrollCount - 1;  
      scrollMargin = cosParameter - cosParameter * Math.cos( scrollCount * scrollStep );
      window.scrollTo( 0, ( scrollHeight - scrollMargin ) );
    } 
    else {

       window.scrollTo( 0,0);
    }; 
  }, 15 );
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
  this.chatService.sendMessage(this.message);
  this.message = '';
}

unixToFormatedDateTime(unixTimestamp: number){
  var date = new Date(unixTimestamp*1000);


    var hours = date.getHours();
    var minutes = "0" + date.getMinutes();
    var seconds = "0" + date.getSeconds();

    var formattedTime = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
    return date.toString();//.substring(0,date.toString().length-30);
  }
  testInt(){
    console.log("interval")
  }
  checkMessage(){
    var msg = this.latestMessage;
    this.messages.push(msg);
    console.log("msg",msg);
    this.pause=true;
    var body = document.body,
    html = document.documentElement;

    var height =  Math.max( body.scrollHeight, body.offsetHeight, 
    html.clientHeight, html.scrollHeight, html.offsetHeight );
    window.scrollTo(0,height);
    setTimeout( () => {
      console.log("releasng pause")
      this.pause=false;
      this.yPos = window.scrollY;
   },4005);
    console.log("adding new object to array");

    msg['imageSrcFocus']=msg['imageSrcFront0'];
    
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

    setInterval( () => {
      var body = document.body,
      html = document.documentElement;

      var height =  Math.max( body.scrollHeight, body.offsetHeight, 
       html.clientHeight, html.scrollHeight, html.offsetHeight );
      if(!this.pause){
       window.scrollTo(0, this.yPos);
       this.yPos+=this.scrollSpeed;
       if(this.yPos >= height || this.yPos <=0 ){
        this.scrollSpeed*=-1;
      }
    }
   },15);


  //  this.chatService.getMessages().subscribe(
  //   (data: any) => this.latestMessage = data
  //   , err => console.error(err), () => this.checkMessage());


   this.chatService
   .getMessages()
   .subscribe(message => {
    console.log("message",message);
    this.latestMessage = message;
    // this.messages.push(message);
    this.checkMessage()
  });


  }
  addTestObj(){
    console.log("adding obj");
    var test = {
      "imageSrcFront0": "1571487646_front_0.jpg",
      "imageSrcFront1": "1571487646_front_1.jpg",
      "imageSrcFront2": "1571487646_front_2.jpg",
      "imageSrcFront3": "1571487646_front_3.jpg",
      "imageSrcTop0": "1571487646_top_0.jpg",
      "dimensions": {
        "width": 1,
        "length": 1,
        "height": 1
      },
      "AI_keys": [{
        "class": "hot tub",
        "score": 0.56,
        "type_hierarchy": "/bathtub/hot tub"
      }, {
        "class": "bathtub",
        "score": 0.561
      }, {
        "class": "automation",
        "score": 0.551
      }, {
        "class": "Swimming Pool",
        "score": 0.508
      }, {
        "class": "Hotel Building",
        "score": 0.504
      }, {
        "class": "conference table",
        "score": 0.501,
        "type_hierarchy": "/furniture/table/conference table"
      }, {
        "class": "table",
        "score": 0.503
      }, {
        "class": "furniture",
        "score": 0.505
      }, {
        "class": "Zamboni  (ice smoothing vehicle in icericks)",
        "score": 0.5,
        "type_hierarchy": "/machine/Zamboni  (ice smoothing vehicle in icericks)"
      }, {
        "class": "machine",
        "score": 0.518
      }, {
        "class": "equipment",
        "score": 0.601
      }, {
        "class": "steel blue color",
        "score": 0.843
      }, {
        "class": "blue color",
        "score": 0.815
      }],
      "colours": [{
        "colour_name": "steel blue",
        "hex": "#4682b4"
      }, {
        "colour_name": "blue",
        "hex": "#0000ff"
      }],
      "accession_time": "1571487646",
      "categories": ["/bathtub/hot tub", "/furniture/table/conference table", "/machine/Zamboni  (ice smoothing vehicle in icericks)"],
      "title": "equipment",
      "similarity": "0.66765976"
    }
    this.accessionObjects.unshift(test);
  }
}
export interface AccessionObjects {
  objects: any[];
}
