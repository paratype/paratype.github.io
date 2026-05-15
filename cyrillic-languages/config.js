/**
 * Runtime configuration.
 *
 * This file is loaded by index.html with a regular <script> tag so that it
 * works even when the app is opened from a local filesystem (file://),
 * where fetch() of plain JSON files is blocked by most browsers.
 *
 * The editor may change the values on the right-hand side below.
 * Keep the JavaScript syntax intact — quotes, commas, braces.
 */
window.__APP_CONFIG = {
    JSON_PATH: "https://raw.githubusercontent.com/paratype-git/cyrillic-languages/master/cyrillic-languages/"
};
