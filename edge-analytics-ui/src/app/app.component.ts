import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { KafkaTestService } from './service/kafka-test.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  private kafkaTestService = inject(KafkaTestService);

  testMessage: string = "";

  title = 'edge-analytics-ui';

  onSendMessage() {
    this.kafkaTestService.postSampleMessage(this.testMessage).subscribe(response => {
      console.log(response);
    });
  }

  onTestKafkaStreams() {
    this.kafkaTestService.postKafkaStreamsWordCount(this.testMessage).subscribe(response => {
      console.log(response);
    });
  }
}
