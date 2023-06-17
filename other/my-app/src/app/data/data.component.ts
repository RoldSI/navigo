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
    const data = { from: 'berlin', to: 'munich' };
    this.http.post('http://localhost:5000/api/data', data).subscribe(
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
