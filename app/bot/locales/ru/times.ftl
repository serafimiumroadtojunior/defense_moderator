minutes = { $count ->
    [one] {$count} минута
    [few] {$count} минуты
   *[other] {$count} минут
}

hours = { $count ->
    [one] {$count} час
    [few] {$count} часа
   *[other] {$count} часов
}

days = { $count ->
    [one] {$count} день
    [few] {$count} дня
   *[other] {$count} дней
}

weeks = { $count ->
    [one] {$count} неделя
    [few] {$count} недели
   *[other] {$count} недель
}