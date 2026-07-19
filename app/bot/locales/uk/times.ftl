minutes = { $count ->
    [one] { $count } хвилину
    [few] { $count } хвилини
   *[other] { $count } хвилин
}

hours = { $count ->
    [one] { $count } годину
    [few] { $count } години
   *[other] { $count } годин
}

days = { $count ->
    [one] { $count } день
    [few] { $count } дні
   *[other] { $count } днів
}

weeks = { $count ->
    [one] { $count } тиждень
    [few] { $count } тижні
   *[other] { $count } тижнів
}