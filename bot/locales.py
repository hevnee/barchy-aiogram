from config import BotConfigs

SUPPORTED_LANGUAGES = (
    "ru", "uk", "en", "pl",
)

SELECTED_LANGUAGE = {
    "ru": { # Russian
        "choose_language": "Язык:",
        "change_language_succesfully": "Язык успешно изменён!",
        
        "welcome_text": (
            f"🤖 Привет! Я бот по имени {BotConfigs.BOT_NAME}.\n"
            "В моём арсенале есть несколько крутых функций!\n"
            "Чтобы их увидеть нужно прописать команду <code>/help</code>"
        ),
        
        "help_text": (
            "🤖 <b>Доступные команды</b>\n\n"
            "⚙️ <b>Основные:</b>\n"
            "<code>/start</code> — Запустить бота\n"
            "<code>/help</code> — Показать это сообщение\n"
            "<code>/language</code> — Сменить язык интерфейса\n\n"
            "💬 <b>ИИ:</b>\n"
            "<code>/style</code> — Изменить стиль поведения ИИ\n"
            "<code>/chat [запрос]</code> — Общение с ИИ\n"
            "<b>Пример:</b> /chat Объясни мне, что такое блокчейн простыми словами.\n"
            "<code>/chatsearch [запрос]</code> — Поиск через интернет + общение с ИИ\n"
            "<b>Пример:</b> /chatsearch последние новости по искусственному интеллекту\n"
            "<code>/forget</code> — Забыть весь текущий диалог\n"
            "<code>/history</code> — Показать историю ваших запросов\n\n"
            "🎲 <b>Игры и активности в чатах:</b>\n"
            "<code>/dick</code> — Измерить размер писюна (играть можно раз в 12 ч)\n"
            "<code>/top_dick</code> — Топ размеров писюна в текущем чате\n"
            "<code>/global_top_dick</code> — Глобальный топ (только в ЛС с ботом)\n"
            "<code>/giveaway [см] [часы]</code> — Создать розыгрыш своих см\n"
            "<b>Пример:</b> /giveaway 100 48 — Создаст розыгрыш 100 см на 48 часов\n"
            "<code>/transfer [@ник|ID] [см]</code> — Передать часть см другому\n"
            "<b>Пример:</b> /transfer @hevnee 3 — Отправит @hevnee 3 см\n\n"
            "ℹ️ Чтобы получить подробности по любой команде, напиши её без аргументов."
        ),

        "just_chat": "Пожалуйста, укажите текст после команды",
        "request_processed": "Ваш запрос обрабатывается...",
        "translating_request": "Переводим ваш запрос...",
        "translator_not_working": "Переводчик не включен",
        "translating_text": "Переводим...",
        "show_original_lang": "Показать оригинал",
        "show_translation_lang": "Показать перевод",
        "position_in_queue": "Позиция в очереди: ",
        "forget_clear": "История разговора очищена!",
        "chatsearch_fetching_data": "Берём данные из интернета...",
        
        "style_normal_button": "Нормальный",
        "style_wise_button": "Мудрый",
        "style_sarcastic_button": "Саркастичный",
        "style_bastard_button": "Ублюдский",
        "style_choose": "Какой стиль ИИ вы бы хотели выбрать?",
        "style_change_succesfully": "Стиль ИИ успешно изменён!",

        "yes": "Да",
        "no": "Нет",
        "prev": "Назад",
        "next": "Вперёд",
        "update_h": "Обновить",
        "request_has_been_deleted": "Запрос был удалён",
        "you_have_no_request": "У вас нету запросов",
        "del_this": "Удалить этот запрос",
        "del_all": "Удалить все запросы",
        "r_u_s_del_this": "Вы уверены что хотите удалить этот запрос?",
        "r_u_s_del_all": "Вы уверены что хотите удалить все запросы?",

        "command_private": "Эту команду можно применять только в <b>чатах (группах)</b>!",
        "invalid_amount": "Укажите корректное число см!",
        "requires_number": "Нужно указать число!",
        "cm": "см",

        "dick_nobody_played": "Пока никто не играл в этом чате",
        "dick_already_played": (
            "Ты уже играл.\n"
            "Текущий размер писюна: {value} см.\n"
            "Следующая попытка через 12 часов!"
        ),
        "dick_grew": "Твой писюн вырос на <b>{value}</b> см.",
        "dick_shrank": "Твой писюн уменьшился на <b>{value}</b> см.",
        "dick_equal_now": (
            "Теперь он равен <b>{value}</b> см.\n"
            "Следующая попытка через 12 часов!"
        ),

        "top_dick_chat_title": "Топ {count} самых больших писюнов в этом чате\n",
        "top_dick_global_title": "Топ {count} самых больших писюнов\n",
        "top_dick_global_private": "Данная команда работает только в личных сообщениях с ботом!",
        
        "giveaway_participate": "Хочу поучавствовать",
        "giveaway_no_longer_active": "Этот розыгрыш больше не действует",
        "giveaway_creator_cannot_join": "Вы не можете быть добавлены, потому что вы создатель этого розыгрыша",
        "giveaway_join_success": "Вы успешно были добавлены в розыгрыш",
        "giveaway_already_joined": "Вы уже участвуете в розыгрыше",
        "giveaway_no_participants": "В розыгрыше этого канала никто не участвовал, поэтому он отменяется.",
        "giveaway_winner_announcement": (
            "И победителем розыгрыша на <b>{giveaway_size}</b> см становится... {mention}!\n"
            "Теперь у него {winner_size} см.\n"
            "Давайте поздравим победителя!"
        ),
        "giveaway_invalid_time_low": "Нельзя ставить время розыгрыша меньше 1 часа!",
        "giveaway_invalid_time_high": "Нельзя ставить время розыгрыша больше 48 часов!",
        "giveaway_insufficient_dick": "У вас недостаточно см, чтобы сделать розыгрыш",
        "giveaway_already_ongoing": "В этом канале уже идёт розыгрыш",
        "giveaway_created": (
            "<b><a href='tg://user?id={user_id}'>{full_name}</a></b> создал(а) розыгрыш на {size} см!\n"
            "Розыгрыш будет действителен {hours} ч.\n"
            "Чтобы участвовать, нажмите кнопку."
        ),

        "transfer_no_args": "Чтобы перевести см, укажите ID или никнейм получателя и количество см",
        "transfer_self": "Вы не можете передать см самому себе!",
        "transfer_user_not_found": "Пользователь не найден в базе данных.",
        "transfer_recipient_not_in_chat": "Команда работает только если получатель есть в этом чате и уже пользовался ботом!",
        "transfer_insufficient_dick": "У вас недостаточно см.",
        "transfer_success_sender": (
            "Вы успешно передали <b>{amount}</b> см пользователю {mention}!\n"
            "У вас осталось <b>{remaining}</b> см."
        ),
        "transfer_success_receiver": (
            "{mention}, пользователь {sender_mention} передал вам <b>{amount}</b> см!\n"
            "Теперь у вас <b>{new_amount}</b> см."
        ),
    },
    # Ukrainian
    "uk": {
        "choose_language": "Мова:",
        "change_language_succesfully": "Мову успішно змінено!",
        
        "welcome_text": (
            f"🤖 Привіт! Я бот на ім'я {BotConfigs.BOT_NAME}.\n"
            "У мене є кілька класних функцій!\n"
            "Щоб їх побачити, введіть команду <code>/help</code>"
        ),
        
        "help_text": (
            "🤖 <b>Доступні команди</b>\n\n"
            "⚙️ <b>Основні:</b>\n"
            "<code>/start</code> — Запустити бота\n"
            "<code>/help</code> — Показати це повідомлення\n"
            "<code>/language</code> — Змінити мову інтерфейсу\n\n"
            "💬 <b>ШІ:</b>\n"
            "<code>/style</code> — Змінити стиль поведінки ШІ\n"
            "<code>/chat [запит]</code> — Спілкуватися з ШІ\n"
            "<b>Приклад:</b> /chat Поясни мені, що таке блокчейн простими словами.\n"
            "<code>/chatsearch [запит]</code> — Пошук в інтернеті + спілкування з ШІ\n"
            "<b>Приклад:</b> /chatsearch останні новини про штучний інтелект\n"
            "<code>/forget</code> — Забути весь поточний діалог\n"
            "<code>/history</code> — Показати історію ваших запитів\n\n"
            "🎲 <b>Ігри та активності в чатах:</b>\n"
            "<code>/dick</code> — Виміряти розмір писюна (грати можна раз на 12 годин)\n"
            "<code>/top_dick</code> — Топ розмірів писюнів у цьому чаті\n"
            "<code>/global_top_dick</code> — Глобальний топ (тільки в ЛС з ботом)\n"
            "<code>/giveaway [см] [години]</code> — Створити розіграш своїх см\n"
            "<b>Приклад:</b> /giveaway 100 48 — Створить розіграш 100 см на 48 годин\n"
            "<code>/transfer [@нік|ID] [см]</code> — Передати частину см іншому\n"
            "<b>Приклад:</b> /transfer @hevnee 3 — Відправить @hevnee 3 см\n\n"
            "ℹ️ Щоб отримати докладну інформацію по будь-якій команді, напишіть її без аргументів."
        ),
        
        "just_chat": "Будь ласка, вкажіть текст після команди",
        "request_processed": "Ваш запит обробляється...",
        "translating_request": "Перекладаємо ваш запит...",
        "translator_not_working": "Перекладач не ввімкнено",
        "translating_text": "Перекладаємо...",
        "show_original_lang": "Показати оригінал",
        "show_translation_lang": "Показати переклад",
        "position_in_queue": "Позиція в черзі: ",
        "forget_clear": "Історія розмови очищена!",
        "chatsearch_fetching_data": "Отримуємо дані з інтернету...",
        
        "style_normal_button": "Нормальний",
        "style_wise_button": "Мудрий",
        "style_sarcastic_button": "Саркастичний",
        "style_bastard_button": "Підлий",
        "style_choose": "Який стиль ШІ ви б хотіли обрати?",
        "style_change_succesfully": "Стиль ШІ успішно змінено!",

        "yes": "Так",
        "no": "Ні",
        "prev": "Назад",
        "next": "Вперед",
        "update_h": "Оновити",
        "request_has_been_deleted": "Запит було видалено",
        "you_have_no_request": "У вас немає запитів",
        "del_this": "Видалити цей запит",
        "del_all": "Видалити всі запити",
        "r_u_s_del_this": "Ви впевнені, що хочете видалити цей запит?",
        "r_u_s_del_all": "Ви впевнені, що хочете видалити всі запити?",

        "command_private": "Цю команду можна використовувати тільки в <b>чатах (групах)</b>!",
        "invalid_amount": "Вкажіть коректне число см!",
        "requires_number": "Потрібно вказати число!",
        "cm": "см",

        "dick_nobody_played": "Поки ніхто не грав у цьому чаті",
        "dick_already_played": (
            "Ви вже грали.\n"
            "Теперішній розмір писюна: {value} см.\n"
            "Наступна спроба через 12 годин!"
        ),
        "dick_grew": "Ваш писюн виріс на <b>{value}</b> см.",
        "dick_shrank": "Ваш писюн зменшився на <b>{value}</b> см.",
        "dick_equal_now": (
            "Тепер він дорівнює <b>{value}</b> см.\n"
            "Наступна спроба через 12 годин!"
        ),

        "top_dick_chat_title": "Топ {count} найбільших писюнів у цьому чаті\n",
        "top_dick_global_title": "Топ {count} найбільших писюнів\n",
        "top_dick_global_private": "Ця команда працює тільки в особистих повідомленнях з ботом!",
        
        "giveaway_participate": "Хочу взяти участь",
        "giveaway_no_longer_active": "Цей розіграш більше не активний",
        "giveaway_creator_cannot_join": "Ви не можете приєднатися, бо ви створювач цього розіграшу",
        "giveaway_join_success": "Ви успішно приєдналися до розіграшу",
        "giveaway_already_joined": "Ви вже берете участь у розіграші",
        "giveaway_no_participants": "У цьому чаті ніхто не брав участі, тож розіграш скасовується.",
        "giveaway_winner_announcement": (
            "І переможцем розіграшу на <b>{giveaway_size}</b> см стаає… {mention}!\n"
            "Тепер у нього {winner_size} см.\n"
            "Вітаємо переможця!"
        ),
        "giveaway_invalid_time_low": "Час розіграшу не може бути менше 1 години!",
        "giveaway_invalid_time_high": "Час розіграшу не може бути більше 48 годин!",
        "giveaway_insufficient_dick": "У вас недостатньо см, щоб зробити розіграш",
        "giveaway_already_ongoing": "У цьому чаті вже є активний розіграш",
        "giveaway_created": (
            "<b><a href='tg://user?id={user_id}'>{full_name}</a></b> створив(а) розіграш на {size} см!\n"
            "Розіграш буде активний {hours} год.\n"
            "Щоб брати участь, натисніть кнопку."
        ),

        "transfer_no_args": "Щоб перевести см, вкажіть ID або нікнейм отримувача та кількість см",
        "transfer_self": "Ви не можете передати см самому собі!",
        "transfer_user_not_found": "Користувача не знайдено у базі даних.",
        "transfer_recipient_not_in_chat": "Команда працює тільки якщо отримувач є в цьому чаті й уже використовував бота!",
        "transfer_insufficient_dick": "У вас недостатньо см.",
        "transfer_success_sender": (
            "Ви успішно передали <b>{amount}</b> см користувачу {mention}!\n"
            "У вас залишилось <b>{remaining}</b> см."
        ),
        "transfer_success_receiver": (
            "{mention}, користувач {sender_mention} передав вам <b>{amount}</b> см!\n"
            "Тепер у вас <b>{new_amount}</b> см."
        ),
    },
    # English
    "en": {
        "choose_language": "Language:",
        "change_language_succesfully": "Language changed successfully!",
        
        "welcome_text": (
            f"🤖 Hello! I\'m a bot named {BotConfigs.BOT_NAME}.\n"
            "I have some cool features!\n"
            "To see them, use the command <code>/help</code>"
        ),
        
        "help_text": (
            "🤖 <b>Available commands</b>\n\n"
            "⚙️ <b>Main:</b>\n"
            "<code>/start</code> — Start the bot\n"
            "<code>/help</code> — Show this message\n"
            "<code>/language</code> — Change interface language\n\n"
            "💬 <b>AI:</b>\n"
            "<code>/style</code> — Change AI behavior style\n"
            "<code>/chat [request]</code> — Chat with AI\n"
            "<b>Example:</b> /chat Explain what blockchain is in simple terms.\n"
            "<code>/chatsearch [request]</code> — Web search + chat with AI\n"
            "<b>Example:</b> /chatsearch latest news on artificial intelligence\n"
            "<code>/forget</code> — Forget the entire current dialogue\n"
            "<code>/history</code> — Show your request history\n\n"
            "🎲 <b>Games and activities in chats:</b>\n"
            "<code>/dick</code> — Measure your dick size (once every 12h)\n"
            "<code>/top_dick</code> — Top dick sizes in this chat\n"
            "<code>/global_top_dick</code> — Global top (private chat only)\n"
            "<code>/giveaway [cm] [hours]</code> — Create a giveaway of your cm\n"
            "<b>Example:</b> /giveaway 100 48 — Creates a giveaway of 100 cm for 48h\n"
            "<code>/transfer [@nick|ID] [cm]</code> — Transfer some cm to another user\n"
            "<b>Example:</b> /transfer @hevnee 3 — Sends 3 cm to @hevnee\n\n"
            "ℹ️ For details on any command, type it without arguments."
        ),

        "just_chat": "Please provide text after the command",
        "request_processed": "Your request is being processed...",
        "translating_request": "Translating your request...",
        "translator_not_working": "Translator is turned off",
        "translating_text": "Translating...",
        "show_original_lang": "Show original",
        "show_translation_lang": "Show translation",
        "position_in_queue": "Position in queue: ",
        "forget_clear": "Conversation history cleared!",
        "chatsearch_fetching_data": "Fetching data from the internet...",
        
        "style_normal_button": "Normal",
        "style_wise_button": "Wise",
        "style_sarcastic_button": "Sarcastic",
        "style_bastard_button": "Bastard",
        "style_choose": "Which AI style would you like to choose?",
        "style_change_succesfully": "AI style changed successfully!",

        "yes": "Yes",
        "no": "No",
        "prev": "Back",
        "next": "Next",
        "update_h": "Update",
        "request_has_been_deleted": "The request has been deleted",
        "you_have_no_request": "You have no requests",
        "del_this": "Delete this request",
        "del_all": "Delete all requests",
        "r_u_s_del_this": "Are you sure you want to delete this request?",
        "r_u_s_del_all": "Are you sure you want to delete all requests?",

        "command_private": "This command can only be used in <b>chats (groups)</b>!",
        "invalid_amount": "Please specify a valid number of cm!",
        "requires_number": "A number is required!",
        "cm": "cm",

        "dick_nobody_played": "No one has played in this chat yet",
        "dick_already_played": (
            "You have already played.\n"
            "Current dick size: {value} cm.\n"
            "Next attempt in 12 hours!"
        ),
        "dick_grew": "Your dick grew by <b>{value}</b> cm.",
        "dick_shrank": "Your dick shrank by <b>{value}</b> cm.",
        "dick_equal_now": (
            "It is now <b>{value}</b> cm.\n"
            "Next attempt in 12 hours!"
        ),

        "top_dick_chat_title": "Top {count} biggest dicks in this chat\n",
        "top_dick_global_title": "Top {count} biggest dicks\n",
        "top_dick_global_private": "This command works only in private messages with the bot!",
        
        "giveaway_participate": "I want to participate",
        "giveaway_no_longer_active": "This giveaway is no longer active",
        "giveaway_creator_cannot_join": "You cannot join because you are the creator of this giveaway",
        "giveaway_join_success": "You have successfully joined the giveaway",
        "giveaway_already_joined": "You are already participating in the giveaway",
        "giveaway_no_participants": "No one participated in this chat giveaway, so it is cancelled.",
        "giveaway_winner_announcement": (
            "And the winner of the giveaway for <b>{giveaway_size}</b> cm is... {mention}!\n"
            "They now have {winner_size} cm.\n"
            "Congratulations to the winner!"
        ),
        "giveaway_invalid_time_low": "Giveaway time cannot be less than 1 hour!",
        "giveaway_invalid_time_high": "Giveaway time cannot be more than 48 hours!",
        "giveaway_insufficient_dick": "You don’t have enough cm to create a giveaway",
        "giveaway_already_ongoing": "A giveaway is already ongoing in this chat",
        "giveaway_created": (
            "<b><a href='tg://user?id={user_id}'>{full_name}</a></b> created a giveaway for {size} cm!\n"
            "The giveaway will last {hours} hours.\n"
            "Click the button to participate."
        ),

        "transfer_no_args": "To transfer cm, provide the recipient’s ID or nickname and the number of cm",
        "transfer_self": "You can’t transfer cm to yourself!",
        "transfer_user_not_found": "User not found in the database.",
        "transfer_recipient_not_in_chat": "This command works only if the recipient is in this chat and has used the bot!",
        "transfer_insufficient_dick": "You don’t have enough cm.",
        "transfer_success_sender": (
            "You have successfully transferred <b>{amount}</b> cm to {mention}!\n"
            "You have <b>{remaining}</b> cm left."
        ),
        "transfer_success_receiver": (
            "{mention}, {sender_mention} transferred you <b>{amount}</b> cm!\n"
            "You now have <b>{new_amount}</b> cm."
        ),
    },
    # Polish
    "pl": {
        "choose_language": "Język:",
        "change_language_succesfully": "Język pomyślnie zmieniony!",
        
        "welcome_text": (
            f"🤖 Cześć! Jestem botem o nazwie {BotConfigs.BOT_NAME}.\n"
            "Mam kilka fajnych funkcji!\n"
            "Aby je zobaczyć, użyj komendy <code>/help</code>"
        ),
        
        "help_text": (
            "🤖 <b>Dostępne komendy</b>\n\n"
            "⚙️ <b>Główne:</b>\n"
            "<code>/start</code> — Uruchom bota\n"
            "<code>/help</code> — Pokaż tę wiadomość\n"
            "<code>/language</code> — Zmień język interfejsu\n\n"
            "💬 <b>AI:</b>\n"
            "<code>/style</code> — Zmień styl działania AI\n"
            "<code>/chat [żądanie]</code> — Rozmawiaj z AI\n"
            "<b>Przykład:</b> /chat Wyjaśnij mi, co to jest blockchain prostymi słowami.\n"
            "<code>/chatsearch [żądanie]</code> — Wyszukiwanie w sieci + rozmowa z AI\n"
            "<b>Przykład:</b> /chatsearch najnowsze wiadomości o sztucznej inteligencji\n"
            "<code>/forget</code> — Zapomnij o całej bieżącej rozmowie\n"
            "<code>/history</code> — Pokaż historię Twoich zapytań\n\n"
            "🎲 <b>Gry i aktywności na czacie:</b>\n"
            "<code>/dick</code> — Zmierz rozmiar penisa (raz na 12h)\n"
            "<code>/top_dick</code> — Lista największych penisów na tym czacie\n"
            "<code>/global_top_dick</code> — Globalna lista (tylko prywatnie)\n"
            "<code>/giveaway [cm] [godziny]</code> — Stwórz rozdanie swoich cm\n"
            "<b>Przykład:</b> /giveaway 100 48 — Rozda 100 cm przez 48h\n"
            "<code>/transfer [@nick|ID] [cm]</code> — Prześlij cm innej osobie\n"
            "<b>Przykład:</b> /transfer @hevnee 3 — Prześle 3 cm do @hevnee\n\n"
            "ℹ️ Aby uzyskać szczegóły dowolnej komendy, wpisz ją bez argumentów."
        ),

        "just_chat": "Proszę podać tekst po komendzie",
        "request_processed": "Twoje żądanie jest przetwarzane...",
        "translating_request": "Tłumaczymy Twoje żądanie...",
        "translator_not_working": "Tłumacz jest wyłączony",
        "translating_text": "Tłumaczymy...",
        "show_original_lang": "Pokaż oryginał",
        "show_translation_lang": "Pokaż tłumaczenie",
        "position_in_queue": "Pozycja w kolejce: ",
        "forget_clear": "Historia rozmowy została wyczyszczona!",
        "chatsearch_fetching_data": "Pobieranie danych z internetu...",
        
        "style_normal_button": "Normalny",
        "style_wise_button": "Mądry",
        "style_sarcastic_button": "Sarkastyczny",
        "style_bastard_button": "Podły",
        "style_choose": "Jaki styl AI chcesz wybrać?",
        "style_change_succesfully": "Styl AI pomyślnie zmieniony!",

        "yes": "Tak",
        "no": "Nie",
        "prev": "Wstecz",
        "next": "Dalej",
        "update_h": "Odśwież",
        "request_has_been_deleted": "Żądanie zostało usunięte",
        "you_have_no_request": "Nie masz żadnych żądań",
        "del_this": "Usuń to żądanie",
        "del_all": "Usuń wszystkie żądania",
        "r_u_s_del_this": "Czy na pewno chcesz usunąć to żądanie?",
        "r_u_s_del_all": "Czy na pewno chcesz usunąć wszystkie żądania?",

        "command_private": "Tej komendy można używać tylko na <b>czatach (grupach)</b>!",
        "invalid_amount": "Podaj prawidłową liczbę cm!",
        "requires_number": "Trzeba podać liczbę!",
        "cm": "cm",

        "dick_nobody_played": "Nikt jeszcze nie grał na tym czacie",
        "dick_already_played": (
            "Już grałeś.\n"
            "Obecny rozmiar penisa: {value} cm.\n"
            "Następna próba za 12 godzin!"
        ),
        "dick_grew": "Twój penis urósł o <b>{value}</b> cm.",
        "dick_shrank": "Twój penis skurczył się o <b>{value}</b> cm.",
        "dick_equal_now": (
            "Teraz ma <b>{value}</b> cm.\n"
            "Następna próba za 12 godzin!"
        ),

        "top_dick_chat_title": "Top {count} największych penisów na tym czacie\n",
        "top_dick_global_title": "Top {count} największych penisów\n",
        "top_dick_global_private": "Ta komenda działa tylko w prywatnych wiadomościach z botem!",
        
        "giveaway_participate": "Chcę wziąć udział",
        "giveaway_no_longer_active": "To rozdanie nie jest już aktywne",
        "giveaway_creator_cannot_join": "Nie możesz dołączyć, ponieważ jesteś twórcą tego rozdania",
        "giveaway_join_success": "Pomyślnie dołączyłeś do rozdania",
        "giveaway_already_joined": "Już bierzesz udział w rozdaniu",
        "giveaway_no_participants": "Nikt nie brał udziału w rozdaniu na tym czacie, więc zostało anulowane.",
        "giveaway_winner_announcement": (
            "Zwycięzcą rozdania na <b>{giveaway_size}</b> cm zostaje... {mention}!\n"
            "Ma teraz {winner_size} cm.\n"
            "Gratulacje dla zwycięzcy!"
        ),
        "giveaway_invalid_time_low": "Czas rozdania nie może być krótszy niż 1 godzina!",
        "giveaway_invalid_time_high": "Czas rozdania nie może być dłuższy niż 48 godzin!",
        "giveaway_insufficient_dick": "Nie masz wystarczająco cm, aby stworzyć rozdanie",
        "giveaway_already_ongoing": "Na tym czacie już trwa rozdanie",
        "giveaway_created": (
            "<b><a href='tg://user?id={user_id}'>{full_name}</a></b> stworzył rozdanie na {size} cm!\n"
            "Rozdanie potrwa {hours} godzin.\n"
            "Kliknij przycisk, aby wziąć udział."
        ),

        "transfer_no_args": "Aby przelać cm, podaj ID lub nick odbiorcy oraz liczbę cm",
        "transfer_self": "Nie możesz przelać cm samemu sobie!",
        "transfer_user_not_found": "Użytkownik nie został znaleziony w bazie danych.",
        "transfer_recipient_not_in_chat": "Ta komenda działa tylko jeśli odbiorca jest na tym czacie i używał już bota!",
        "transfer_insufficient_dick": "Nie masz wystarczająco cm.",
        "transfer_success_sender": (
            "Pomyślnie przelałeś <b>{amount}</b> cm użytkownikowi {mention}!\n"
            "Zostało Ci <b>{remaining}</b> cm."
        ),
        "transfer_success_receiver": (
            "{mention}, {sender_mention} przelał Ci <b>{amount}</b> cm!\n"
            "Masz teraz <b>{new_amount}</b> cm."
        ),
    },
    
    "none": "Выбери язык"
}