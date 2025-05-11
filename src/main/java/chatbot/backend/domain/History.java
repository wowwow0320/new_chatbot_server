package chatbot.backend.domain;

import jakarta.persistence.*;
import lombok.*;

import java.util.Date;

@Entity
@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class History {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int pid;
    private String ask;
    @Lob
    @Column(columnDefinition = "TEXT")
    private String answer;
    private Date askCreatedAt;
    private Date answerCreatedAt;
}
