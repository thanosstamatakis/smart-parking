import { Component, OnInit } from '@angular/core';
import { Chart } from 'chart.js';

@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.scss']
})
export class ReportComponent implements OnInit {

  chart: any;

  dataPoints : Object =[{x: 10,y: 20}, {x: 15,y: 10}]
  labels = ['x','y'];

  constructor() { }

  ngOnInit() {
    
    console.log(this.dataPoints);

    this.chart = new Chart(document.getElementById('lineChart'), {
      type: 'line',
      data: {
        labels: this.labels,
        datasets: [{
          label: 'x',
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
        }}
    });

    console.log(this.chart);

   }

}