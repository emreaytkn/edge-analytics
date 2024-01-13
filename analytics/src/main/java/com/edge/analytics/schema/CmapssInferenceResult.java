package com.edge.analytics.schema;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
public class CmapssInferenceResult {

    @JsonProperty("prediction")
    private int prediction;

    @JsonProperty("experimentId")
    private String experimentId;

}
