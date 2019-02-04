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

  labels = ['00:00','01:00','02:00','03:00','04:00','05:00','06:00','07:00','08:00','09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00','22:00','23:00'];


  constructor(public activeModal: NgbActiveModal) {}

  ngOnInit() { 
    var blockPopulation = this.blockData.population;
    var blockCentroid = this.blockData.centroid;
    var dataPoints = new Array();
    var dataPointsFixed = new Array();

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
