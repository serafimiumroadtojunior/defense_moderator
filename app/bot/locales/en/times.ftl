minutes = { $count ->
    [one] { $count } minute
   *[other] { $count } minutes
}

hours = { $count ->
    [one] { $count } hour
   *[other] { $count } hours
}

days = { $count ->
    [one] { $count } day
   *[other] { $count } days
}

weeks = { $count ->
    [one] { $count } week
   *[other] { $count } weeks
}