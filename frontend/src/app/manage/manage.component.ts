import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpEventType, HttpResponse } from '@angular/common/http';
import { DataService } from '../data.service';
import { NgbProgressbarConfig } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-manage',
  templateUrl: './manage.component.html',
  styleUrls: ['./manage.component.scss']
})
export class ManageComponent implements OnInit {

  selectedFile: File = null;

  upload_msg: number = null;

  show: Boolean = true;

  fileName: string = "";

  onFileSelected(event) {
    this.selectedFile = this.data.FileSelected(event);
    this.fileName = this.selectedFile.name;
  }

  onUpload() {
    this.data.UploadFile(this.selectedFile).subscribe(
      (event) => {
        if (event.type === HttpEventType.UploadProgress) {
          const percentDone = Math.round(100 * event.loaded / event.total);
          this.upload_msg = percentDone;
          this.show = (percentDone == 100);
        }
      }, (error) => {
        console.log('Error sending file to server: ', error);
      });

  }

  constructor(private data: DataService, config: NgbProgressbarConfig) {
    config.max = 100;
    config.striped = true;
    config.animated = true;
    config.type = 'success';
    config.height = '20px';
  }

  ngOnInit() {
  }



}
