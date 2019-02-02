import { Component, OnInit, Input } from '@angular/core';
import { NgbActiveModal, NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { Chart } from 'chart.js';

@Component({
  selector: 'app-modal-content',
  templateUrl: './modal-content.component.html',
  styleUrls: ['./modal-content.component.scss']
})
export class ModalContentComponent implements OnInit {

  @Input() blockData;

  chart: any;

  blockPopulation: number;
  blockCentroid: String;

  // dataPoints : Object =[{x: 10,y: 20}, {x: 15,y: 10}]
  labels = ['00:00','01:00','02:00','03:00','04:00','05:00','06:00','07:00','08:00','09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00','22:00','23:00'];

  dataPoints: Object = [
{x:0, y: 0.18},
{x:1, y: 0.17},
{x:2, y: 0.21},
{x:3, y: 0.25},
{x:4, y: 0.22},
{x:5, y: 0.17},
{x:6, y: 0.16},
{x:7, y: 0.39},
{x:8, y: 0.54},
{x:9, y: 0.77},
{x:10, y: 0.78},
{x:11, y: 0.83},
{x:12, y: 0.78},
{x:13, y: 0.78},
{x:14, y: 0.8},
{x:15, y: 0.76},
{x:16, y: 0.78},
{x:17, y: 0.79},
{x:18, y: 0.84},
{x:19, y: 0.57},
{x:20, y: 0.38},
{x:21, y: 0.24},
{x:22, y: 0.19},
{x:23, y: 0.23}
]

  constructor(public activeModal: NgbActiveModal) {}

  ngOnInit() { 
    var blockPopulation = this.blockData.population;
    var blockCentroid = this.blockData.centroid;

    this.blockPopulation = blockPopulation;
    this.blockCentroid = blockCentroid;
    
    console.log(this.dataPoints);
    this.chart = new Chart(document.getElementById('lineChart'), {
      type: 'line',
      data: {
        labels: this.labels,
        bezierCurve: false,
        datasets: [{
          label: 'Demand',
          data: this.dataPoints,
          borderColor: "#ffcc00"
        },]
      },
      options: {
        legend: {
          display: false
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
          easing: 'easeOutBounce',
          numSteps: 60,
          duration: 10000,
        }
      }
    });


  }

}
