import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { io, Socket } from 'socket.io-client';

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private url = 'http://localhost:3000';
  private socket;

  constructor() {
      this.socket = io(this.url);
  }

  public sendMessage(message: string) {
      this.socket.emit('new-message', message);
  }

  public getMessages = () => {
      // return Observable.create((observer) => {
      //     this.socket.on('new-message', (message) => {
      //         observer.next(message);
      //     });
      // });
      return new Observable(observer => {
        this.socket.on('new-message', msg => {
          observer.next(msg);
        });
      });
  }
}