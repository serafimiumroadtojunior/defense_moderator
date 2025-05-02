mute-user = 
    👀<b><a href='tg://user?id={$user_id}'>{$user_full_name}</a> is muted for {$measure_time}</b>
    <b>Reason: {$reason}</b>
    <b>Admin: <a href='tg://user?id={$admin_id}'>{$admin_full_name}</a></b>

ban-user =
    👀<b><a href='tg://user?id={$user_id}'>{$user_full_name}</a> is banned for {$measure_time}</b>
    <b>Reason: {$reason}</b>
    <b>Admin: <a href='tg://user?id={$admin_id}'>{$admin_full_name}</a></b>

spam-percent-ban=
    👀<b><a href='tg://user?id={$user_id}'>{$user_full_name}</a> was banned for a high percentage of spam messages ({$messages_percent}%)</b>

banned-reactions = 
    👀<b><a href='tg://user?id={$user_id}'>{$user_full_name}</a> was banned for 30 minutes for exceeding the number of reactions</b>

badwords-muting = 
    👀<b><a href='tg://user?id={$user_id}'>{$user_full_name}</a> was muted for using banned words</b>

abuse-welcome = 
    👀<b><a href='tg://user?id={$user_id}'>{$user_full_name}</a> was muted for trying to bypass the mute</b>

unique-words =
    👀<b><a href='tg://user?id={$user_id}'>{$user_full_name}</a> was muted for exceeding the coefficient of non-unique words</b>

unique-messages =
    👀<b><a href='tg://user?id={$user_id}'>{$user_full_name}</a> was muted for exceeding the number of non-unique messages</b>