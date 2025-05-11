package chatbot.backend.dto;

import jakarta.persistence.Column;
import jakarta.persistence.Lob;
import lombok.Data;
import lombok.Setter;

@Data
@Setter
public class TextDto {
    private String ask;
    @Lob
    @Column(columnDefinition = "TEXT")
    private String answer;
}
