import { Component, OnInit } from '@angular/core';
import * as L from 'leaflet';
import { DataService } from '../data.service';
import { NgbActiveModal, NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { ModalContentComponent } from '../modal-content/modal-content.component';
import { ModalContentUnauthorizedComponent } from '../modal-content-unauthorized/modal-content-unauthorized.component';
import { AuthService } from '../auth.service';
import { SimulationService } from '../simulation.service';


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
  polygonLayer: L.FeatureGroup;


  constructor(private _data: DataService, private _modalService: NgbModal, private _auth: AuthService, private _sim: SimulationService) { }



  insertToString = function insertToString(main_string, ins_string, pos) {
    if (typeof (pos) == "undefined") {
      pos = 0;
    }
    if (typeof (ins_string) == "undefined") {
      ins_string = '';
    }
    return main_string.slice(0, pos) + ins_string + main_string.slice(pos);
  }

  sanitizeCoords = function sanitizeCoords(coords, insertToString) {
    var members;

    if (coords == "0") {
      coords = "[0]";
    } else {
      coords = (coords.replace(/[{()}]/g, ''));
      coords = (coords.replace(/[{,}]/g, ''));

      members = coords.split(" ");

      var i;
      coords = "";
      for (i = 0; i < (members.length); i += 2) {
        coords += " , [" + members[i + 1] + ", " + members[i] + "]";
      }

      coords = coords.replace(' , ', '');
      coords = insertToString(coords, '[', 0);
      coords = insertToString(coords, ']', coords.length);
    }
    return coords;
  }

  sanitizeName = function sanitizeName(name) {
    name = name.replace('population_data_per_block.', '');
    return name;
  }

  getCurrentTime() {
    let formatedTime: number = 0;
    let date = new Date();
    let hours = date.getHours();
    let minutes = date.getMinutes();

    formatedTime = hours + 0.01 * minutes;

    return formatedTime;
  }

  formatCurrentTime(time: Object) {
    return time['hour'] + 0.01 * time['minute'];
  }

  createMap(mapName: string) {
    let cityMap = L.map('cityMap', {
      zoomControl: false
    }).setView([40.62023756670292, 22.95810400084713], 17);

    return cityMap;
  }

  addTileLayer(mapName: L.Map) {
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
      attribution: null,
    }).addTo(mapName);
  }

  async getInitColors(time) {
    var colors = await this._data.getColors(time);
    return colors;
  }

  async refreshPolygons(cityMap: L.Map, polygonLayer: L.FeatureGroup, time) {
    var colors = await this.getInitColors(this.formatCurrentTime(time));
    for (var itteration in polygonLayer['_layers']) {
      polygonLayer['_layers'][itteration]['options']['fillColor'] = colors[polygonLayer['_layers'][itteration]['polygonNumber']];
    }
    cityMap.removeLayer(polygonLayer);
    polygonLayer.addTo(cityMap);
  }

  runSimulation(cityMap: L.Map, polygonLayer: L.FeatureGroup, time) {
    // this.removePolygons(cityMap, polygonLayer);
    this.refreshPolygons(cityMap, polygonLayer, time);
  }

  async ngOnInit() {
    var colors = await this.getInitColors(this.getCurrentTime());

    // Fetch polygons from api through the data service
    this._data.getPolygons().subscribe(data => {
      this.apiData = data;


      // Initialize simulation options globally
      this._sim.setSimOptions({
        runSimulations: false,
        time: { hour: 0, minute: 0 }
      });


      // Subscribe to the global current options from the simulation service
      this._sim.currentOptions.subscribe(res => {
        if (res['runSimulations']) { this.runSimulation(cityMap, polygonLayer, res['time']); }
      });


      //Initiate user status (if user is admin or not)
      this._auth.currentToken.subscribe(res => {
        this.isAdmin = res['isAdmin'];
      });


      // Create map and add to viewport
      const cityMap = this.createMap('cityMap');


      // Add tile layer to map
      this.addTileLayer(cityMap);


      // Get the bootstrap _modalService 
      var theModalRef = this._modalService;
      var polygon;
      var polygonToAdd;
      var polygonLayer = new L.FeatureGroup();

      for (var itteration in this.apiData) {
        //declarations inside the loop
        let polygonSpecs = (this.apiData[itteration]);
        polygonSpecs['id'] = parseInt(itteration);


        //Get polygon data that was received through the service, sanitize the data so it is readable from leaflet functions
        this.apiData[itteration].polygon = this.sanitizeCoords(this.apiData[itteration].polygon, this.insertToString);
        polygon = JSON.parse(this.apiData[itteration].polygon);


        //Check if a block has polygon data and draw it
        if (polygon[0] != 0) {
          polygonToAdd = L.polygon(polygon, { fillColor: colors[itteration], stroke: false, fillOpacity: 0.18 });
          polygonToAdd['polygonSpecs'] = polygonSpecs;
          polygonToAdd['polygonNumber'] = parseInt(itteration);
          polygonToAdd.addTo(polygonLayer);


          //Define action for click on an itteration polygon
          polygonToAdd.on('click', event => {
            let polygonNumber = event.target.polygonNumber;
            let polygonSpecs = event.target.polygonSpecs;

            if (this.isAdmin) {
              var theModalData = theModalRef.open(ModalContentComponent, {
                size: 'lg'
              });
            } else {
              var theModalData = theModalRef.open(ModalContentUnauthorizedComponent, {
                size: 'lg'
              });
            }

            theModalData.componentInstance.polygonSpecs = polygonSpecs;

          });
        }
      }
      polygonLayer.addTo(cityMap);
    });
  }

}
