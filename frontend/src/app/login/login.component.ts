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
  btnColor: string="primary";

  constructor(private _fb: FormBuilder, private _data: DataService, private _router: Router, private _auth: AuthService) { 

    this.rForm = _fb.group({
      username: [null, Validators.required],
      password: [null, Validators.required]
   });
  
  }

  callLoginUser(post) {
    var type: String = '';
    if (post.username == 'admin'){
      type = 'admin';
    }else{
      type = 'normal'
    }
    let body = {
      type: type,
      username: post.username,
      password: post.password
    }

    this._auth.loginUser(body).subscribe(res => {
      if (res['Token'] == null){
        // failed login
        this.btnColor = 'danger';
        this._auth.getUserData();
      }else{
        // successful login
        this.btnColor = 'success';
        this._auth.storeToken(res);
        this._auth.getUserData();
        this._router.navigate(['']);
      }

    });

  }

}
