import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class DataService {

  selectedFile: File = null;

  constructor(private _http: HttpClient) { }

  getPolygons(): Observable<object> {
    return this._http.get('http://localhost:8080/api/placemark/all');
  }

  async getColors(time: number) {
    let params = new HttpParams()
      .set('time', time.toString());
    let colorPromise = await this._http.get('http://localhost:8080/api/placemark/availability/color', { params: params }).toPromise();
    let colors = Promise.resolve(colorPromise);
    return colors;

  }

  FileSelected(event) {
    this.selectedFile = <File>event.target.files[0];
    console.log(this.selectedFile);
    return this.selectedFile;
  }

  UploadFile(file: File) {
    let formData = new FormData();
    formData.append('kml-file', file, file.name);
    return this._http.post('http://localhost:8080/api/placemark/file', formData,
      {
        reportProgress: true,
        observe: 'events'
      });
  }

  FlushDB() {
    return this._http.delete('http://localhost:8080/api/placemark/all',
      {
        reportProgress: true,
        observe: 'events'
      });
  }

  async getPolygonDemand(polygonId) {
    let demandPromise = await this._http.get('http://localhost:8080/api/placemark/demand/' + polygonId).toPromise();
    let demand = Promise.resolve(demandPromise);
    return demand;
  }




}
