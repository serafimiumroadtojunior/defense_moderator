from pathlib import Path
from typing import List, Dict, Tuple, Union

from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub

from app.bot.config import LOCALES_DIR, Locale


def get_ftl_paths(path: Path) -> list[Path]:
    paths: List = []

    if not path.exists(): 
        return paths
    for file in path.iterdir(): 
        if file.is_dir(): 
            paths.extend(get_ftl_paths(file))
        elif file.suffix == ".ftl":
            paths.append(file)

    return paths


def init_translator_hub() -> TranslatorHub:
    locales_map: Dict[Locale, Tuple[Union[Locale, str]]] = {
        locale: (locale, "ru", "en") 
        for locale in Locale
    }

    translators: List[FluentTranslator] = [
        FluentTranslator(
            locale,
            translator=FluentBundle.from_files(
                locale, filenames=get_ftl_paths(LOCALES_DIR / locale)
            ),
        )
        for locale in Locale
    ]

    translator_hub: TranslatorHub = TranslatorHub(
        locales_map=locales_map,  
        translators=translators, 
    )

    return translator_hub