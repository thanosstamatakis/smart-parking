import { Injectable } from '@angular/core';
import { HttpClient, HttpEventType, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
// import { Subject } from 'rxjs/Subject';
// import 'rxjs/add/operator/map';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  selectedFile: File = null;

  constructor(private http: HttpClient) { }

  getLanguages() {
    return this.http.get('http://localhost:8080/api/placemark/')
  }

  FileSelected(event) {
    this.selectedFile = <File>event.target.files[0];
    console.log(this.selectedFile);
    return this.selectedFile;
  }

  UploadFile(file: File) {
    let formData = new FormData();
    formData.append('kml-file', file, file.name);
    return this.http.post('http://localhost:8080/api/placemark/', formData,
      {
        reportProgress: true,
        observe: 'events'
      });
  }

}
