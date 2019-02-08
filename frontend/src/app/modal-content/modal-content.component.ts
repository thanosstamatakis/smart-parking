import { Component, OnInit, Input } from '@angular/core';
import { NgbActiveModal, NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { Chart } from 'chart.js';
import { compileNgModuleFactory__POST_R3__ } from '@angular/core/src/application_ref';

@Component({
  selector: 'app-modal-content',
  templateUrl: './modal-content.component.html',
  styleUrls: ['./modal-content.component.scss']
})
export class ModalContentComponent implements OnInit {

  @Input() blockData;

  chart: any;

  time: Object = {hour: 0, minute: 0};
  value: any = null;

  blockPopulation: number;
  blockCentroid: String;
  liveDemand: number = null;

  labels = ['00:00','01:00','02:00','03:00','04:00','05:00','06:00','07:00','08:00','09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00','22:00','23:00'];

  timeClick() {
    console.log(this.time);
  }

  getValue (event) {
    console.log(event['valueAsNumber']);
    this.liveDemand = event['valueAsNumber'];
  }

  timePickerInput(event){
    console.log(event.originalTarget.textContent);

    // console.log(event);
    // console.log(event.originalTarget.previousElementSibling);
    // console.log(event.originalTarget.nextElementSibling);

    if (event.originalTarget.previousElementSibling){
      console.log(event.originalTarget.previousElementSibling.value);
    }else{
      console.log(event.originalTarget.nextElementSibling.value);
    }


    var action:string = event.originalTarget.textContent; 
    switch(action) { 
      case "Increment minutes": { 
          this.time['minute'] = +event.originalTarget.nextElementSibling.value; 
          break; 
      } 
      case "Decrement minutes": { 
          this.time['minute'] = +event.originalTarget.previousElementSibling.value; 
          break; 
      } 
      case "Increment hours": {
          this.time['hour'] = +event.originalTarget.nextElementSibling.value;
          break;    
      } 
      case "Decrement hours": { 
          this.time['hour'] = +event.originalTarget.previousElementSibling.value;
          break; 
      }  
      default: { 
          console.log("Invalid choice"); 
          break;              
      } 
    }


  }

  constructor(public activeModal: NgbActiveModal) {}

  ngOnInit() { 


    var blockPopulation = this.blockData.population;
    var blockCentroid = this.blockData.centroid;
    var dataPoints = new Array();
    var dataPointsFixed = new Array();

    this.liveDemand = 100*this.blockData.demand[0];

    for (var individual in this.blockData.demand) {
      dataPoints.push({'y': this.blockData.demand[individual]});
      dataPointsFixed.push({'y': this.blockData.fixed_demand[individual]})
    }

    this.blockPopulation = blockPopulation;
    this.blockCentroid = blockCentroid;
    
    this.chart = new Chart(document.getElementById('lineChart'), {
      type: 'line',
      data: {
        labels: this.labels,
        bezierCurve: false,
        datasets: [{
          label: 'Demand',
          data: dataPoints,
          borderColor: "#FFA922"
        },{
          label: 'Fixed Demand',
          data: dataPointsFixed,
          borderColor : '#1BC97A'
        }]
      },
      options: {
        legend: {
          display: true
        },
        scales: {
          xAxes: [{
            display: true
          }],
          yAxes: [{
            display: true
          }]
        },
        animation: {
          easing: 'easeOutBounce'
        }
      }
    });


  }

}
