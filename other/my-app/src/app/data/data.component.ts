import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-data',
  templateUrl: './data.component.html',
  styleUrls: ['./data.component.css'],
})
export class DataComponent implements OnInit {
  responseData: any;

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.getData();
  }

  getData(): void {
    this.http.get('http://localhost:5000/api/data').subscribe(
      (response) => {
        console.log(response);
        this.responseData = response;
      },
      (error) => {
        console.error(error);
      }
    );
  }
}
