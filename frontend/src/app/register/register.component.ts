import { Component } from '@angular/core';
import { FormBuilder, FormGroup, FormControl, Validators, AbstractControl } from '@angular/forms';
import { PasswordValidation } from './password-validation';
import { DataService } from '../data.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})


export class RegisterComponent {

  rForm: FormGroup;
  postUser: any;
  description: string="";
  password :string="";
  username: string="";
  confirm_password: string="";


  constructor(private _fb: FormBuilder, private _data: DataService) {

    this.rForm = _fb.group({
      username: [null, Validators.required],
      validate: '',
      password: [null, Validators.compose([
        // 1. Password Field is Required
        Validators.required,
        // 2. check whether the entered password has a number
        Validators.pattern(/\d/),
        // 3. check whether the entered password has upper case letter
        Validators.pattern(/[A-Z]/),
        // 4. check whether the entered password has a lower-case letter
        Validators.pattern(/[a-z]/),
        // 5. check whether the entered password has a special character
        Validators.pattern(/[ !@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/),
        // 6. Has a minimum length of 6 characters
        Validators.minLength(6)])
     ],
     confirm_password: [null, Validators.required]
    },{
      validator: PasswordValidation.MatchPassword
    });

  }

  addUser(post) {
    // this.password = post.password;
    // this.username = post.username;
    // this.type = '';
    let body = {
      type: 'normal',
      username: post.username,
      password: post.password
    }

    this._data.addUser(body).subscribe(data => {
      console.log(data);
    });

  }

}

