import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { Observable } from 'rxjs';
import { AuthService } from '../app/auth.service';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(private _auth: AuthService, private _router: Router) {}

  async canActivate(){
    let checkRole = await this._auth.checkToken();
    let isAdmin = this._auth.getUserData()['isAdmin'];    

    if (checkRole == false || isAdmin == false){
      this._router.navigate(['login']);
      return false;
    }else{
      return true;
    }

  }

}
