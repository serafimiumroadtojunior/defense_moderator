add_warn = 
    👀<b><a href='tg://user?id={$user_id}'>{$user_full_name}</a> отримує попередження, причина: {$reason}</b>
    <b><i>Кількість попередженнь: {$warns}</i></b>
    <b>Адмін: <a href='tg://user?id={$admin_id}'>{$admin_full_name}</a></b>

finally_warn = 
    👀<b><a href='tg://user?id={$user_id}'>{$user_full_name}</a> отримує мут на 30 хвилин через превіщення кількості попередженнь</b>
    <b>Адмін: <a href='tg://user?id={$admin_id}'>{$admin_full_name}</a></b>

warn-reason =
    📝<b>Причина попередження: {$reason}</b>

user-reasons=
    👀<b>Причини попереджень <a href='tg://user?id={$user_id}'>{$user_full_name}</a></b>
    {$warns_reasons}

delete-warn = 
    👀<b>Попередження <a href='tg://user?id={$user_id}'>{$user_full_name}</a> було видалено</b>
    <b>Адмін: <a href='tg://user?id={$admin_id}'>{$admin_full_name}</a></b>

not-reason = 
    👀<b>Причина не вказана</b>