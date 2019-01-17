import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpProgressEvent, HttpEventType, HttpResponse } from '@angular/common/http';

@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.scss']
})
export class ReportComponent implements OnInit {

  selectedFile: File = null;

  upload_msg: string = "";

  onFileSelected(event){
    this.selectedFile = <File>event.target.files[0];
    console.log(this.selectedFile);
  }

  onUpload(){
    let formData = new FormData();
    formData.append('kml-file', this.selectedFile, this.selectedFile.name);
    console.log(formData);
    this.http.post('http://localhost:8080/api/placemark/', formData, 
    {reportProgress: true,
    observe: 'events'})
    .subscribe((event) => {
      if (event.type === HttpEventType.UploadProgress) {
          const percentDone = Math.round(100 * event.loaded / event.total);
          const upload_msg = `${percentDone}% Uploaded`;
          console.log(typeof(upload_msg));
      }
    }, (error) => {
      console.log('Error', error);
    });

  }

  constructor(private http: HttpClient) { }
  
  ngOnInit() {
    
  }



}
