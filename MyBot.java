import org.telegram.telegrambots.bots.TelegramLongPollingBot;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;

public class MyBot extends TelegramLongPollingBot {

    @Override
    public void onUpdateReceived(Update update) {
        if (update.hasMessage() && update.getMessage().hasText()) {
            String messageText = update.getMessage().getText();
            long chatId = update.getMessage().getChatId();

            if (messageText.equals("/start")) {
                sendDepartmentsMessage(chatId);
            } else if (messageText.equals("/department1")) {
                sendCoursesMessage(chatId, "Department 1");
            } else if (messageText.equals("/department2")) {
                sendCoursesMessage(chatId, "Department 2");
            }
        }
    }

    private void sendDepartmentsMessage(long chatId) {
        SendMessage message = new SendMessage()
                .setChatId(chatId)
                .setText("Please select a department:")
                .setReplyMarkup(KeyboardUtils.getDepartmentsKeyboardMarkup());
        
        try {
            execute(message);
        } catch (TelegramApiException e) {
            e.printStackTrace();
        }
    }

    private void sendCoursesMessage(long chatId, String department) {
        SendMessage message = new SendMessage()
                .setChatId(chatId)
                .setText("Courses under " + department + ":\nCourse 1\nCourse 2\nCourse 3");
        
        try {
            execute(message);
        } catch (TelegramApiException e) {
            e.printStackTrace();
        }
    }

    @Override
    public String getBotUsername() {
        // Return your bot's username
        return "agency";
    }

    @Override
    public String getBotToken() {
        // Return your bot's token
        return "6447901778:AAHMl6cviQbAZ8C5S5WyfzXOWSjdHif8En4";
    }
}
