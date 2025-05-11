package chatbot.backend.service;

import chatbot.backend.domain.History;
import chatbot.backend.repository.HistoryRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Date;

@Service
@RequiredArgsConstructor
public class HistoryService {
    private final HistoryRepository historyRepository;

    public String runPythonScript(String ask) throws IOException, InterruptedException {

        Date nowAsk = new Date();

        ProcessBuilder processBuilder = new ProcessBuilder("python3", "scripts/script.py", ask);
        processBuilder.redirectError(ProcessBuilder.Redirect.DISCARD);
//        processBuilder.redirectErrorStream(true);
        Process process = processBuilder.start();

        // 결과 읽기
        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        StringBuilder result = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            result.append(line).append("\n");
        }

        int exitCode = process.waitFor(); // 동기 처리 (여기서 기다림)
        if (exitCode != 0) {
            System.out.println("result : " + result.toString().trim());
            throw new RuntimeException("Python script failed with exit code " + exitCode);
        }
        History history = new History();
        history.setAsk(ask);
        history.setAnswer(result.toString().trim());
        history.setAskCreatedAt(nowAsk);

        Date nowAnswer = new Date();
        history.setAnswerCreatedAt(nowAnswer);
        historyRepository.save(history);
        return result.toString().trim();
    }




}
