import { Injectable } from '@angular/core';
import { JwtHelperService } from '@auth0/angular-jwt';
import { BehaviorSubject } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Router } from '@angular/router';


@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private _http: HttpClient, private _router: Router) { }

  
  private realTimeToken = new BehaviorSubject<Object>(null);
  public currentToken = this.realTimeToken.asObservable();

  //Function that returns the user data (type, username) and emmits its value to an observable.
  //This means that every component can have real-time usertype and username through this service.
  getUserData () {
    let token = this.getJWT();
    let tokenData: Object = null;
    
    if(token == null){
      //if no one is signed in
      tokenData = {
        'username': 'guest',
        'isAdmin': false,
        'isLoggedIn': false
      };
 
    }else{
      //if someone signed in

      let decodedToken = this.decodeJWT(token);

      //get values from the token
      tokenData = {
        'username': this.getUserName(decodedToken),
        'isAdmin': this.checkAdmin(decodedToken),
        'isLoggedIn': this.checkLoggedIn(decodedToken)
      };
    }

    //Emmiting the tokenData through this rxJS Behaviour Subject.
    this.realTimeToken.next(tokenData);
    return tokenData;
 
  }

  //check if the logged in user is of type admin
  checkAdmin(decodedToken) {
    return decodedToken['username'] == 'admin';
  }

  // find if a user is logged in from the token payload contents if they exist
  checkLoggedIn (decodedToken) {
    let response: Boolean = false;
    if (decodedToken['type'] == 'admin' || decodedToken['type'] == 'normal'){
      response = true;
    }
    return response;
  }

  // method to get the user name from the token payload
  getUserName (decodedToken) {
    let response: String = decodedToken.username;
    return response;
  }

  // method to retrieve the JSON Web Token from the local storage
  getJWT() {
  let token = localStorage.getItem('token');
  return token;
  }

   //method to decode the JSON Web Token that has been given as input
  decodeJWT (token) {
    const helper = new JwtHelperService();
    let decodedToken: Object = helper.decodeToken(JSON.stringify(token));
    console.log(decodedToken);
    return decodedToken;
  }
  
  //method to store the JWT token with value 'token' from local storage
  storeToken (response) {
    localStorage.setItem('token', JSON.stringify(response['Token']));
  }

   //method to add user with given body from registerform
   registerUser(body) {
  let params = new HttpParams()
    .set('type',body.type)
    .set('username',body.username)
    .set('password',body.password)

  return this._http.post('http://localhost:8080/api/user/adduser',null,{params: params});
  }

  //method that logs out the user
  logoutUser () {
    localStorage.removeItem('token');
    //this function is used to reset the global variables username, isAdmin, isLoggedIn
    this._router.navigate(['']);
    this.getUserData();
  }

  //method that checks if a token has been tampered with
  async checkToken(){
    let userData: object;
    if (localStorage.getItem('token')==null){
      return false;
    }else {
      userData = this.getUserData();
      let token = localStorage.getItem('token');
      let type: string = '';
      if (userData['isAdmin'] == true){
        type = 'admin';
      }else{
        type = 'normal';
      }
      let params = new HttpParams()
      .set('token',token.substring(1, token.length - 1))
      .set('type',type)
      .set('username',userData['username']);
  
      let authPromise = await this._http.get('http://localhost:8080/api/user/validation/token',{params: params}).toPromise()
      let auth = Promise.resolve(authPromise);

      return auth;
    }

  }

  //method that logs in the user with the given body from the form
  loginUser(body) {
    let params = new HttpParams()
    .set('type',body.type)
    .set('username',body.username)
    .set('password',body.password)

    return this._http.get('http://localhost:8080/api/user/validation',{params: params});
  }

}
