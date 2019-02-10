import { Component, OnInit } from '@angular/core';
import * as L from 'leaflet';
import { DataService } from '../data.service';
import { NgbActiveModal, NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ModalContentComponent } from '../modal-content/modal-content.component';
import { ModalContentUnauthorizedComponent } from '../modal-content-unauthorized/modal-content-unauthorized.component';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {


  //Object to hold data from DataService
  apiData: Object;
  visibleModal: Boolean = false;
  modalReference: Object = this._modalService;
  isAdmin: Boolean = this._auth.getUserData()['isAdmin'];

  constructor(private _data: DataService, private _modalService: NgbModal, private _auth: AuthService) { }



  insertToString = function insertToString(main_string, ins_string, pos) {
    if(typeof(pos) == "undefined") {
      pos = 0;
    }
    if(typeof(ins_string) == "undefined") {
      ins_string = '';
    }
    return main_string.slice(0, pos) + ins_string + main_string.slice(pos);
  }  

  sanitizeCoords = function sanitizeCoords(coords, insertToString) {
    var members;

    if (coords == "0"){
      coords = "[0]";
    }else{
      coords = (coords.replace(/[{()}]/g, ''));
      coords = (coords.replace(/[{,}]/g, ''));

      members = coords.split(" ");

      var i;
      coords="";
      for (i = 0; i < (members.length); i+=2) {
          coords += " , ["+members[i+1]+", "+members[i]+"]";
      }

      coords = coords.replace(' , ','');
      coords = insertToString(coords ,'[', 0);
      coords = insertToString(coords ,']', coords.length);
    }
    return coords;
  }

  sanitizeName = function sanitizeName(name) {
    name = name.replace('population_data_per_block.','');
    return name;
  }
 
  getBlockColor(block: Object){
    let slots = parseInt(block['parking_slots']);
    let demand = block['demand'];
    let population = parseInt(block['population']);
    let color: string = ''; 
    var d = new Date();
    let time = d.getHours();

    if (!this.isAdmin){
      if ((population*0.2) >= slots) {
        color = 'red';
      } else {
        let available = slots - 0.2*population;
        available = Math.round(available - demand[time]*available);
        let percentage = 100 - Math.round((available/slots)*100);
        // console.log(percentage+"%");
          if (percentage <= 59){
            color = 'green';
          }else if (percentage <= 84 ) {
            color = 'yellow';
          }else{
            color = 'red';
          }
      }
    } else {
      color = 'black';
    }

    return color;

  }

  createMap(mapName: string){
    let cityMap = L.map('cityMap',{
      zoomControl: false
    }).setView([40.62023756670292, 22.95810400084713], 17);

    return cityMap;
  }

  addTileLayer(mapName: L.Map){
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png',{ 
      attribution: null,
    }).addTo(mapName);
  }

  ngOnInit() {

    //Initiate user status (if user is admin or not)
    this._auth.currentToken.subscribe(res => {
      this.isAdmin = res['isAdmin'];
      // console.log('This is from home component.')
      // console.log(this.isAdmin);
    });

    // Create map and add to viewport
    const cityMap = this.createMap('cityMap');

    // Add tile layer to map
    this.addTileLayer(cityMap);

    // Get the bootstrap _modalService 
    var theModalRef = this._modalService;
    
    this._data.getLanguages().subscribe(data => {this.apiData = data;

      var blockCoords;
      var blockToDraw;

      for (var individual in this.apiData) {
        //declarations inside the loop
        let blockData = (this.apiData[individual]);
       
       
        //Get polygon data that was received through the service, sanitize the data so it is readable from leaflet functions
        this.apiData[individual].polygon = this.sanitizeCoords(this.apiData[individual].polygon, this.insertToString);
        blockCoords = JSON.parse(this.apiData[individual].polygon);

        //Check if a block has polygon data and draw it
        if (blockCoords[0]!=0){
          blockToDraw = L.polygon(blockCoords, {fillColor: this.getBlockColor(this.apiData[individual]), stroke: false, fillOpacity:0.18});
          blockToDraw['blockData'] = blockData;
          blockToDraw.addTo(cityMap);

          
          //Define action for click on an individual polygon
          blockToDraw.on('click', function(event){

            let blockData = event.target.blockData;
            if (this.isAdmin){
              var theModalData = theModalRef.open(ModalContentComponent,{
                size: 'lg'
              });
            }else{
              var theModalData = theModalRef.open(ModalContentUnauthorizedComponent,{
                size: 'lg'
              });
            }
            theModalData.componentInstance.blockData = blockData;
          });
        }


      }
    });
  }

}
