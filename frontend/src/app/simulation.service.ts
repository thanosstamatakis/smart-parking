import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SimulationService {

  private modalOptions = new BehaviorSubject<Object>(null);
  public currentOptions = this.modalOptions.asObservable();

  setSimOptions(options) {
    this.modalOptions.next(options);
  }

  constructor() { }
}
