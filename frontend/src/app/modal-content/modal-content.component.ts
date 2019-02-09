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
  displayTime: Date = new Date("T0:0");
  drawTime: String = (this.displayTime.toLocaleTimeString(['en-US'], {hour: '2-digit', minute:'2-digit'})).toString();
  value: any = null;

  blockPopulation: number;
  blockCentroid: String;
  liveDemand: number = null;

  labels: String[] = ['00:00','01:00','02:00','03:00','04:00','05:00','06:00','07:00',
                      '08:00','09:00','10:00','11:00',' 12:00','13:00','14:00','15:00',
                      '16:00','17:00','18:00','19:00','20:00','21:00','22:00','23:00'];

  timeClick() {
    console.log(this.time);
    console.log(this.blockData.demand[this.time['hour']]);
    this.blockData.demand[this.time['hour']] = (this.liveDemand/100).toString();
    console.log(this.blockData.demand[this.time['hour']]);
  }

  setValue (event) {
    console.log(event['valueAsNumber']);
    this.liveDemand = event['valueAsNumber'];
  }

  timePickerInput(event){
    console.log(this.time);
    this.setDisplayTime(this.time);
    this.setDrawTime(['en-US'], {hour: '2-digit', minute:'2-digit'});
    this.setDemand(this.time);
    console.log(this.liveDemand);
    console.log(this.displayTime.toLocaleTimeString(['en-US'], {hour: '2-digit', minute:'2-digit'}));

  }

  // method to set the displayTime date variable hours and minutes (that's all we need) 
  setDisplayTime(time) {
    this.displayTime.setHours(time['hour']);
    this.displayTime.setMinutes(time['minute']);
  }

  // method to set the locale time to be drawn as a String
  setDrawTime(locales: string[], options: Object){
    this.drawTime = (this.displayTime.toLocaleTimeString(locales, options)).toString();
  }

  // method to get demand given the time 
  setDemand(timeToFetchDemand: Object) {
    let demand: number;
    let hour: number = timeToFetchDemand['hour'];
    let minute: number = timeToFetchDemand['minute'];
    let nextHour: number;

    // assign the next hour (for the special case that hour is 23)

    if (hour == 23){
      nextHour = 0;
    }else{
      nextHour++;
    }

    // assign demand as percentage depending on the minutes

    if (minute <= 30) {
      demand = (this.blockData.demand[hour])*100;
    }else {
      demand = (this.blockData.demand[nextHour])*100  ;
    }
    this.liveDemand = demand;
  }

  constructor(public activeModal: NgbActiveModal) {}

  ngOnInit() { 


    var blockPopulation = this.blockData.population;
    var blockCentroid = this.blockData.centroid;
    var dataPoints = new Array();
    var dataPointsFixed = new Array();

    this.liveDemand = 100*this.blockData.demand[0];

    this.displayTime.toLocaleTimeString();
    console.log(this.displayTime.toLocaleTimeString());

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
