add_warn =
    👀<b><a href='tg://user?id={$user_id}'>{$user_full_name}</a> receives a warning for: {$reason}.</b>
    <b><i>Number of warnings: {$warns}.</i></b>
    <b>Admin: <a href='tg://user?id={$admin_id}'>{$admin_full_name}</a></b>

finally_warn = 
    👀<b><a href='tg://user?id={$user_id}'>{$user_full_name}</a> is muted for 30 minutes due to exceeding the warning limit.</b>
    <b>Admin: <a href='tg://user?id={$admin_id}'>{$admin_full_name}</a></b>

warn-reason =
    📝<b>Warning reason: {$reason}</b>

user-reasons=
    👀<b>Warning reasons for <a href='tg://user?id={$user_id}'>{$user_full_name}</a></b>
    {$warns_reasons}

delete-warn = 
    👀<b>Warning for <a href='tg://user?id={$user_id}'>{$user_full_name}</a> has been deleted.</b>
    <b>Admin: <a href='tg://user?id={$admin_id}'>{$admin_full_name}</a></b>

not-reason = 
    👀<b>Reason not specified</b>