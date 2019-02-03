import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
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
    return this.http.get('http://localhost:8080/api/placemark/all')
  }

  FileSelected(event) {
    this.selectedFile = <File>event.target.files[0];
    console.log(this.selectedFile);
    return this.selectedFile;
  }

  UploadFile(file: File) {
    let formData = new FormData();
    formData.append('kml-file', file, file.name);
    return this.http.post('http://localhost:8080/api/placemark/file', formData,
      {
        reportProgress: true,
        observe: 'events'
      });
  }

  FlushDB(){
    return this.http.delete('http://localhost:8080/api/placemark/all',
    {
      reportProgress: true,
      observe: 'events'
    });
  }

  addUser(body) {
    console.log(body.type);
    let params = new HttpParams()
      .set('type',body.type)
      .set('username',body.username)
      .set('password',body.password)

    return this.http.post('http://localhost:8080/api/user/adduser',null,{params: params});
  }

}
