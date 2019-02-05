import { Component } from '@angular/core';
import { DataService } from '../data.service';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, FormControl, Validators, AbstractControl } from '@angular/forms';
import { JwtHelperService } from '@auth0/angular-jwt';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {

  rForm: FormGroup;
  password :string="";
  username: string="";

  constructor(private _fb: FormBuilder, private _data: DataService, private _router: Router) { 

    this.rForm = _fb.group({
      username: [null, Validators.required],
      password: [null, Validators.required]
   });
  
  }

  refresh(): void {
    this._router.navigate(['']);
    window.location.reload();
    
  }

  loginUser(post) {
    let body = {
      type: 'normal',
      username: post.username,
      password: post.password
    }

    this._data.loginUser(body).subscribe(res => {
      console.log(res);
      console.log(res['Token'])
      var token = JSON.stringify(res['Token']);
      const helper = new JwtHelperService();
      let decodedToken = helper.decodeToken(token);
      console.log(decodedToken);
    });

  }

}
