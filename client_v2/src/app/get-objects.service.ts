
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class GetObjectsService {
//   objectsUrl = 'assets/test_objects.json';

//   constructor(private http: HttpClient) {
//       // this.socket = io(this.url);
//   }

//   public	getObjects() {
//   return this.http.get(this.objectsUrl);
// }

constructor(private http: HttpClient) { }
dataUrl = 'http://localhost:9999/accession/assets/objects.json';

getObjects() {
  return this.http.get(this.dataUrl);
}  
  
}