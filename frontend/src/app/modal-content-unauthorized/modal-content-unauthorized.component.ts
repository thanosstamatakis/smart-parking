import { Component, OnInit, Input, Output } from '@angular/core';
import { NgbActiveModal, NgbModal, NgbTab, NgbTabset } from '@ng-bootstrap/ng-bootstrap';
import { Chart } from 'chart.js';
import { polygon } from 'leaflet';
import { DataService } from '../data.service';
import { SimulationService } from '../simulation.service';

@Component({
  selector: 'app-modal-content-unauthorized',
  templateUrl: './modal-content-unauthorized.component.html',
  styleUrls: ['./modal-content-unauthorized.component.scss']
})
export class ModalContentUnauthorizedComponent implements OnInit {

  //Get input from parent element
  @Input() polygonSpecs;
  @Output() result;

  //initialization
  chart: any;
  demand: Object = null;
  time: Object = { hour: 0, minute: 0 };
  displayTime: Date = new Date("T0:0");
  drawTime: String = (this.displayTime.toLocaleTimeString(['en-US'], { hour: '2-digit', minute: '2-digit' })).toString();
  value: any = null;
  blockPopulation: number;
  blockCentroid: String;
  liveDemand: number = null;
  labels: String[] = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00',
    '08:00', '09:00', '10:00', '11:00', ' 12:00', '13:00', '14:00', '15:00',
    '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'];

  timeClick() {
    console.log(this.time);
    console.log(this.demand[this.time['hour']]);
    this.demand[this.time['hour']] = (this.liveDemand / 100).toString();
    console.log(this.demand[this.time['hour']]);
  }

  setValue(event) {
    console.log(event['valueAsNumber']);
    this.liveDemand = event['valueAsNumber'];
  }

  timePickerInput(event) {
    console.log(this.time);
    this.setDisplayTime(this.time);
    this.setDrawTime(['en-US'], { hour: '2-digit', minute: '2-digit' });
    this.setDemand(this.time);
  }

  // method to set the displayTime date variable hours and minutes (that's all we need) 
  setDisplayTime(time) {
    this.displayTime.setHours(time['hour']);
    this.displayTime.setMinutes(time['minute']);
  }

  // method to set the locale time to be drawn as a String
  setDrawTime(locales: string[], options: Object) {
    this.drawTime = (this.displayTime.toLocaleTimeString(locales, options)).toString();
  }

  // method to get demand given the time 
  setDemand(timeToFetchDemand: Object) {
    let demand: number;
    let hour: number = timeToFetchDemand['hour'];
    let minute: number = timeToFetchDemand['minute'];
    let nextHour: number;

    // assign the next hour (for the special case that hour is 23)

    if (hour == 23) {
      nextHour = 0;
    } else {
      nextHour++;
    }

    // assign demand as percentage depending on the minutes

    if (minute <= 30) {
      demand = (this.demand[hour]) * 100;
    } else {
      demand = (this.demand[nextHour]) * 100;
    }
    this.liveDemand = parseFloat(demand.toFixed(1));
    console.log(this.liveDemand);
  }

  async getDemand(id) {
    var demand = await this._data.getPolygonDemand(id);
    return demand;
  }

  closeAndSubmit() {
    this._sim.setSimOptions({
      runSimulations: true,
      time: this.time
    });
    this.activeModal.close('Close click')
  }


  constructor(public activeModal: NgbActiveModal, private _data: DataService, private _sim: SimulationService) { }

  async ngOnInit() {

    var demand = await this.getDemand(this.polygonSpecs.id);
    var dataPoints = demand['demand'];
    var dataPointsFixed = demand['fixed_demand'];
    var blockPopulation = this.polygonSpecs.population;

    this.liveDemand = parseFloat((100 * dataPoints[0]).toFixed(1));
    this.demand = demand['demand'];
    this.displayTime.toLocaleTimeString();
    this.blockPopulation = blockPopulation;
    this.chart = new Chart(document.getElementById('lineChart'), {
      type: 'line',
      data: {
        labels: this.labels,
        datasets: [{
          label: 'Demand',
          data: dataPoints,
          borderColor: "#007bff",
          lineTension: 0.000000001
        }, {
          label: 'Fixed Demand',
          data: dataPointsFixed,
          borderColor: '#1BC97A'
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
