package chatbot.backend.repository;

import chatbot.backend.domain.History;
import org.springframework.data.jpa.repository.JpaRepository;

public interface HistoryRepository extends JpaRepository<History, Long> {
}
