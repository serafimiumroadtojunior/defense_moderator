add_warn = 
    👀<b><a href='tg://user?id={$user_id}'>{$user_full_name}</a> получает предупреждение по причине: {$reason}.</b>
    <b><i>Количество предупреждений: {$warns}</i></b>
    <b>Админ: <a href='tg://user?id={$admin_id}'>{$admin_full_name}</a></b>

finally_warn = 
    👀<a href='tg://user?id={$user_id}'><b>{$user_full_name}</b></a> был навсегда забанен за получение 3 предупреждений.
    <b>Админ: <a href='tg://user?id={$admin_id}'>{$admin_full_name}</a></b>

warn-reason =
    📝<b>Причина предпуреждения: {$reason}</b>

user-reasons=
    👀<b>Причины предупреждений\({$warns}\) <a href='tg://user?id={$user_id}'>{$user_full_name}</a></b>
    {$warns_reasons}

delete-warn = 
    👀<b>Предупреждение <a href='tg://user?id={$user_id}'>{$user_full_name}</a> было удалено.</b>
    <b>Админ: <a href='tg://user?id={$admin_id}'>{$admin_full_name}</a></b>

not-reason = 
    👀<b>Причина не указана</b>