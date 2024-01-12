import { HttpClient } from "@angular/common/http";
import { inject, Injectable } from "@angular/core";
import { Observable } from "rxjs";

@Injectable({
    providedIn: 'root',
})
export class KafkaTestService {

    private http = inject(HttpClient);

    private readonly kafkaTestUrl = 'http://localhost:8096/api/kafka/test'

    constructor() {}

    postSampleMessage(message: string): Observable<any> {
        return this.http.post<any>(this.kafkaTestUrl, message);
    }

}