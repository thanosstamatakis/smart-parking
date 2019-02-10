import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavComponent } from './nav/nav.component';
import { ContactComponent } from './contact/contact.component';
import { HomeComponent } from './home/home.component';
import { ReportComponent } from './report/report.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { ManageComponent } from './manage/manage.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { ModalContentComponent } from './modal-content/modal-content.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ModalContentUnauthorizedComponent } from './modal-content-unauthorized/modal-content-unauthorized.component';


@NgModule({
  declarations: [
    AppComponent,
    NavComponent,
    ContactComponent,
    HomeComponent,
    ReportComponent,
    ManageComponent,
    LoginComponent,
    RegisterComponent,
    ModalContentComponent,
    ModalContentUnauthorizedComponent
  ],
  entryComponents: [
    ModalContentComponent,
    ModalContentUnauthorizedComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    NgbModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
