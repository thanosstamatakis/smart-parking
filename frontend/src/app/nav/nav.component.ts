import { Component, Input, OnInit, SimpleChanges } from '@angular/core';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-nav',
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.scss']
})
export class NavComponent implements OnInit {

  appTitle: string = 'myapp';

  //Initiallization
  data: Object = this._auth.getUserData();

  callLogout() {
    console.log('logging out.');
    this._auth.logoutUser();
  }

  constructor(private _auth: AuthService) { }

  ngOnInit() {
    //subscribe the navbar data object to the response of the authentication service
    this._auth.currentToken.subscribe(res => {
      this.data = res;
      console.log('Navbar - this is the value:')
      console.log(this.data);
    })
  }


}
