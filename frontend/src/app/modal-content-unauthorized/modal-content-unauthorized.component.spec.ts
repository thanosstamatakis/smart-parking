import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ModalContentUnauthorizedComponent } from './modal-content-unauthorized.component';

describe('ModalContentUnauthorizedComponent', () => {
  let component: ModalContentUnauthorizedComponent;
  let fixture: ComponentFixture<ModalContentUnauthorizedComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ModalContentUnauthorizedComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ModalContentUnauthorizedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
