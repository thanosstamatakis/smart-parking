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

  // public postFile(fileToUpload: File): {[filekey:string]:Observable<number>} {
  //   const endpoint = 'http://localhost:8080/api/placemark/';
  //   const formData: FormData = new FormData();
  //   const progress = new Subject<number>();
  //   const status = {};

  //   formData.append('fileKey', fileToUpload, fileToUpload.name);

  //   const req = new HttpRequest('POST', endpoint, formData, {
  //     reportProgress: true
  //   });

  //   this.http.request(req).subscribe(event => {
  //     if (event.type === HttpEventType.UploadProgress) {
  //       const percentDone = Math.round(100 * event.loaded / event.total);
  //       progress.next(percentDone);
  //     } else if (event instanceof HttpResponse) {
  //       progress.complete();
  //     }
  //   });

  //   status[fileToUpload.name] = {
  //     progress: progress.asObservable()
  //   };

  //   return status;
  //   // return this.http.post(endpoint, formData, { headers: yourHeadersConfig })
  //   //   .map(() => { return true; })
  //   //   .catch((e) => this.handleError(e));
  // }

}
