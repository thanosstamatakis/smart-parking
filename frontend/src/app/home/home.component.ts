import { Component, OnInit } from '@angular/core';
import * as L from 'leaflet';
import { DataService } from '../data.service';
import { Observable } from 'rxjs';
import { async } from 'q';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {


  //Object to hold data from DataService
  languages$: Object;

  
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
  constructor(private data: DataService) { }

  ngOnInit() {
    this.data.getLanguages().subscribe(data => {this.languages$ = data;

      var polygonCoordData;
      var polygonToDraw;

      // Create map and add to viewport
      const myfrugalmap = L.map('frugalmap',{
        zoomControl: false
      }).setView([40.62023756670292, 22.95810400084713], 17);

      // Add tile layer to map
      L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png',{ 
        attribution: null,
      }).addTo(myfrugalmap);


      for (var individual in this.languages$) {
        var blockNumber;
        var blockPopulation;
        this.languages$[individual].polygon = this.sanitizeCoords(this.languages$[individual].polygon, this.insertToString);
        polygonCoordData = JSON.parse(this.languages$[individual].polygon);
        if (polygonCoordData[0]!=0){
          polygonToDraw = L.polygon(polygonCoordData, {color: 'black'});
          polygonToDraw.addTo(myfrugalmap);
          blockNumber = this.sanitizeName(this.languages$[individual].name);
          blockPopulation = this.languages$[individual].population;
          polygonToDraw.bindPopup("<b><h5>This is block: "+blockNumber+"</h5></b> " + "<br>"
                                   +"<h7>Block Population: "+blockPopulation+"</h7><br>"
                                   +'<a href="#" class="btn btn-outline-primary">Go somewhere</a>');
        }
      }
    });
  }

}
