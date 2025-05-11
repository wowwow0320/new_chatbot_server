package chatbot.backend.controller;

import chatbot.backend.dto.TextDto;
import chatbot.backend.service.HistoryService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

@Controller
@RequiredArgsConstructor
public class HistoryController {
    private final HistoryService historyService;

    @PostMapping("/ask")
    public ResponseEntity<?> askQuestion(@RequestBody TextDto textDto) {
        try {
            String response = historyService.runPythonScript(textDto.getAsk());
            textDto.setAnswer(response);
            return ResponseEntity.ok(textDto);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("오류: " + e.getMessage());
        }
    }



}
