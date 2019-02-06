import { Component } from '@angular/core';
import { DataService } from '../data.service';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../auth.service';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {

  rForm: FormGroup;
  password :string="";
  username: string="";

  constructor(private _fb: FormBuilder, private _data: DataService, private _router: Router, private _auth: AuthService) { 

    this.rForm = _fb.group({
      username: [null, Validators.required],
      password: [null, Validators.required]
   });
  
  }

  callLoginUser(post) {
    let body = {
      type: 'normal',
      username: post.username,
      password: post.password
    }

    this._auth.loginUser(body).subscribe(res => {
      this._auth.storeToken(res);
      this._auth.getUserData();
      this._router.navigate(['']);
    });

  }

}
