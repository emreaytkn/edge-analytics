import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { KafkaTestService } from './service/kafka-test.service';
import { CmapssInferenceResult } from './model/cmapss-model';

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
  cmapssInferenceResults: CmapssInferenceResult[] = []

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

  onGetCmapssExperimentResults() {
    this.kafkaTestService.getAllCmapssInferenceResults().subscribe((response: CmapssInferenceResult[]) => {
      this.cmapssInferenceResults = response;
      console.log(response[0].experimentId);
    });
  }

  isInfo(result: CmapssInferenceResult): boolean {
    return result.prediction >= 120 ? true:false;
  }

  isWarning(result: CmapssInferenceResult): boolean {
    return (result.prediction < 120 && result.prediction > 65) ? true:false;
  }

  isError(result: CmapssInferenceResult): boolean {
    return (result.prediction <= 65) ? true:false;
  }
}
