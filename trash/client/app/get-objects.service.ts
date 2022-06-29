import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable()
// export class GetObjectsService {
// 	objectsUrl = 'assets/objects.json';
//   constructor(private http: HttpClient) { }
  

// 	public	getObjects() {
// 	  return this.http.get(this.objectsUrl);
// 	}
// }

export class GetObjectsService {
    objectsUrl = 'assets/objects.json';

    constructor(private http: HttpClient) {
        // this.socket = io(this.url);
    }

    public	getObjects() {
	  return this.http.get(this.objectsUrl);
	}

    
    
}