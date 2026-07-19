mute-user = 
    👀<b><a href='tg://user?id={$user_id}'>{$user_full_name}</a> получает мут на {$measure_time}</b>
    <b>Причина: {$reason}</b>
    <b>Админ: <a href='tg://user?id={$admin_id}'>{$admin_full_name}</a></b>

ban-user =
    👀<b><a href='tg://user?id={$user_id}'>{$user_full_name}</a> получает бан на {$measure_time}</b>
    <b>Причина: {$reason}</b>
    <b>Админ: <a href='tg://user?id={$admin_id}'>{$admin_full_name}</a></b>

spam-percent-ban=
    👀<b><a href='tg://user?id={$user_id}'>{$user_full_name}</a> был забанен за высокий процент спам-сообщений ({$messages_percent}%)</b>

banned-reactions = 
    👀<b><a href='tg://user?id={$user_id}'>{$user_full_name}</a> был забанен на 30 минут за превышение количества реакций</b>

badwords-muting = 
    👀<b><a href='tg://user?id={$user_id}'>{$user_full_name}</a> был замучен за использование запрещенных слов</b>

abuse-welcome = 
    👀<b><a href='tg://user?id={$user_id}'>{$user_full_name}</a> был замучен за попытку обхода мута</b>

unique-words =
    👀<b><a href='tg://user?id={$user_id}'>{$user_full_name}</a> был замучен за превышение коефицента неуникальных слов</b>

unique-messages =
    👀<b><a href='tg://user?id={$user_id}'>{$user_full_name}</a> был замучен за превышение количества неуникальных сообщений</b>