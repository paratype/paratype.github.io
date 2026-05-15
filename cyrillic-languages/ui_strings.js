/**
 * Localized UI strings. Each field is an array of two items:
 *   [ "English text", "Русский текст" ].
 *
 * This file is loaded by index.html with a regular <script> tag so that it
 * works even when the app is opened from a local filesystem (file://).
 *
 * The editor may change the string values on the right-hand side.
 * Keep the JavaScript syntax intact — quotes, commas, braces, brackets.
 */
window.__APP_UI_STRINGS = {
    MAIN_MENU: {
        logo: ["Language reference:", "Справочник языков:"],
        about: ["About", "О проекте"],
        languages: ["Languages", "Языки"],
        panCyr: ["Pan-", "Вся "],
        definitions: ["Definitions", "Определения"],
        select: ["Select language", "Выберите язык"]
    },
    LANG_TITLES_RED: {
        latinNames: ["Latin names:", "Латинские названия:"],
        langGroups: ["Language groups:", "Языковые группы:"]
    },
    LEGEND_BTNS: {
        case: ["Upper", "Upper", "Lower", "Lower"],
        serif: ["Serif", "Serif", "Sans", "Sans"],
        italic: ["Normal", "Normal", "Italic", "Italic"],
        sort: ["Alphabet", "Алфавит", "Unicodes", "Юникоды"],
        textTable: ["Text table", "Таблица"],
        parameters: ["Parameters", "Параметры"],
        sortTitle: ["Sort", "Сортировка"]
    },
    SELECTED: {
        title: ["Selected languages", "Выбранные языки"],
        reset: ["Reset selection", "Сброс выбора"],
        none: ["none", "ничего не выбрано"]
    },
    DOWNLOAD: ["Download", "Скачать"],
    TABLE: {
        upper: ["Uppercase", "Прописные"],
        lower: ["Lowercase", "Строчные"],
        glyph: ["Glyph", "Символ"],
        description: ["Description", "Описание"],
        unicodes: ["Unicodes", "Юникоды"],
        italic: ["italic", "курсивное начертание"],
        normal: ["normal", "прямое начертание"]
    }
};
