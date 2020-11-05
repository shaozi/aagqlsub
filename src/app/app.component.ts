import { Component } from '@angular/core';
import { WebSocketMessage } from 'rxjs/internal/observable/dom/WebSocketSubject';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  subscriptions: {
    id: number;
    counter: number;
    gqlSocket: WebSocketSubject<any>;
    done: boolean;
    error: boolean;
  }[] = [];

  ngOnInit() {}
  sub() {
    let id = Math.floor(Math.random() * 100000);

    let gqlSocket = webSocket({
      url: 'ws://localhost:8000',
      protocol: 'graphql-ws',
    });
    let subscription = {
      id: id,
      counter: 0,
      gqlSocket: gqlSocket,
      done: false,
      error: false,
    };
    this.subscriptions.push(subscription);
    // optional. This will cause server to send a connection_ack
    gqlSocket.next({ type: 'connection_init', payload: {} });

    let query = `subscription {
     counter
    }`;

    gqlSocket.subscribe(
      (response: any) => {
        switch (response.type) {
          case 'connection_ack':
            console.log('connection ack');
            break;
          case 'complete':
            console.log(`sub id ${response.id} completed`);
            subscription.done = true;
            break;
          case 'data':
            subscription.counter = response.payload.data.counter;
            break;
          default:
            // not parsed
            console.log(response);
        }
      },
      (error) => {
        console.error(error);
        subscription.error = true;
        subscription.done = true;
      },
      () => {
        // interrupted
        console.log('ws is closed for whatever reason');
        subscription.done = true;
      }
    );
    // start subscription
    gqlSocket.next({
      id: id,
      type: 'start',
      payload: {
        query: query,
      },
    });
  }
}
