import { Component } from '@angular/core';
import { ChatService } from '../chat.service';
import { GetObjectsService } from './get-objects.service';
import { MasonryModule } from 'angular2-masonry';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  message: string;
  messages: string[] = [];
  yPos: number = 0;
  scrollSpeed = 1;
  pause: boolean = false;
  accessionObjects: AccessionObjects ={"objects":[]}
  collection = [];
  imgSrc: string = "assets/images/0F8A3627.JPG";
  constructor(private chatService: ChatService, private objectsService: GetObjectsService) {

  }

  updateObjectStructure(){
   // console.log("got objects",this.accessionObjects)
    for (var i = 0; i < this.accessionObjects.objects.length; i++) {
      console.log(this.accessionObjects.objects[i].categories);

    }
  }
  getTopCategory(item){
    var category = "";
    // console.log("item",item)
    for(var category in item.categories){
      var exploded = item.categories[category].split("/")
      // console.log ("explodeed", exploded[1]);
      category = exploded[1];
    }
    return category;
    // var exploded = this.accessionObjects.objects[i].categories[category].split("/")
  }
  onSubscribe(data){
    // console.log("on data",data)
    var categories = [];
    this.accessionObjects = data;
     // console.log("got objects",this.accessionObjects)
     for (var i = 0; i < this.accessionObjects.objects.length; i++) {
      // console.log(this.accessionObjects.objects[i]);
      // console.log(this.accessionObjects.objects[i].categories);
      if( this.accessionObjects.objects[i].categories !== undefined ){
        // console.log(typeof this.accessionObjects.objects[i].categories)

        for(var category in this.accessionObjects.objects[i].categories){
         var exploded = this.accessionObjects.objects[i].categories[category].split("/")
         if( categories.includes(exploded[1]) == false){
          categories.push(exploded[1])
        }

      }

    }

  }
  console.log(categories)
}

scrollToTop(scrollDuration) {
  // var height = Math.max( body.scrollHeight, body.offsetHeight, 
  //  html.clientHeight, html.scrollHeight, html.offsetHeight );
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
      // this.scrollToBottom(scrollDuration);
    }

  }, 15 );
}
scrollToBottom(scrollDuration) {
  var body = document.body,
  html = document.documentElement;

  var height = Math.max( body.scrollHeight, body.offsetHeight, 
   html.clientHeight, html.scrollHeight, html.offsetHeight );
  //console.log("scrolling to bottom",window.innerHeight);
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
       // clearInterval(scrollInterval);
      // console.log("scrolling to top");
       // this.scrollToTop(scrollDuration);
       window.scrollTo( 0,0);
      // scrollToBottom(scrollDuration);
    }; 
  }, 15 );
}
shuffle(a) {
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
  this.accessionObjects.objects.unshift(test);
}
unixToFormatedDateTime(unixTimestamp){
  var date = new Date(unixTimestamp*1000);


    // Hours part from the timestamp
    var hours = date.getHours();
    // Minutes part from the timestamp
    var minutes = "0" + date.getMinutes();
    // Seconds part from the timestamp
    var seconds = "0" + date.getSeconds();

    // Will display time in 10:30:23 format
    var formattedTime = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
    return date.toString().substring(0,date.toString().length-30);
  }
  testInt(){
    console.log("interval")
  }
  checkMessage(msg){
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
     // this.scrollToBottom(10000);
   },10005);

    this.accessionObjects.objects.push(msg);
    this.updateObjectStructure();
  }
  // showConfig() {
  // this.objectsService.getObjects()
  //   .subscribe( 
  //     (data: AccessionObjects) => this.accessionObjects = { ...data } ) ;
  // }
  showConfig() {
    this.objectsService.getObjects()
    .subscribe( 
      (data: AccessionObjects) => this.onSubscribe( { ...data }) ) ;
  }
  // updateCollection() {
  // this.objectsService.getObjects()
  //   .subscribe( this.updateObjectStructure() ) ;
  // }

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
     //  console.log(this.yPos,height,this.scrollSpeed);
       if(this.yPos >= height || this.yPos <=0 ){
        this.scrollSpeed*=-1;
      }
    }
     // this.scrollToBottom(10000);
   },15);
   // this.scrollToBottom(100000);
   this.chatService
   .getMessages()
   .subscribe((message: string) => {
    this.messages.push(message);
    this.checkMessage(message)
  });
    //   setInterval(function(){ 
    //   console.log(this.accessionObjects);
    //   // this.accessionObjects.objects = this.shuffle(this.accessionObjects.objects);
    // }, 3000);

  }
}
export interface AccessionObjects {
  objects: any[];
}