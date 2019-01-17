import { Injectable } from '@angular/core';
import { HttpClient, HttpRequest, HttpEventType, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
// import { Subject } from 'rxjs/Subject';
// import 'rxjs/add/operator/map';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  constructor(private http: HttpClient) { }

  getLanguages() {
    // return this.http.get('http://127.0.0.1:8080/languages/api/json')
    return this.http.get('http://localhost:8080/api/placemark/')
  }
}
