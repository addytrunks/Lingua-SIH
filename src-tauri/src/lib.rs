use base64::prelude::*;
use minreq::get;
use percent_encoding::{utf8_percent_encode, AsciiSet, CONTROLS};
use rust_translate::translate;

const FRAGMENT: &AsciiSet = &CONTROLS.add(b' ').add(b'"').add(b'<').add(b'>').add(b'`');

#[tauri::command]
fn get_languages() -> [[&'static str; 2]; 11] {
    return [
        ["Bengali", "bn"],
        ["Gujarati", "gu"],
        ["Hindi", "hi"],
        ["Kannada", "kn"],
        ["Malayalam", "ml"],
        ["Marathi", "mr"],
        ["Nepali", "ne"],
        ["Punjabi", "pa"],
        ["Telugu", "te"],
        ["Urdu", "ur"],
        ["Tamil", "ta"],
        // ["French", "fr"],
        // ["German", "de"],
        // ["Italian", "it"],
        // ["Japanese", "ja"],
        // ["Korean", "ko"],
        // ["Russian", "ru"],
        // ["Spanish", "es"],
        // ["Chinese", "zh"],
        // ["Arabic", "ar"],
        // ["English", "en"],
        // ["Morse Code", "mc"],
    ];
}

#[tauri::command]
async fn get_translated(lang_code: &str, text: &str) -> Result<String, ()> {
    let translated_text = translate(text, "en", lang_code).await.ok();
    match translated_text {
        Some(s) => Ok(s),
        None => Err(()),
    }
}

#[tauri::command]
fn texttoaudio(lang_code: &str, text: &str) -> String {
    let len = text.len();
    let text = utf8_percent_encode(text, FRAGMENT).to_string();

    if let Ok(rep) = get(format!("https://translate.google.fr/translate_tts?ie=UTF-8&q={}&tl={}&total=1&idx=0&textlen={}&client=tw-ob", text,lang_code, len)).send().inspect_err(|e| println!("{:?}",e)) {
        let mut bytes = rep.as_bytes();
        let audio_data = BASE64_STANDARD.encode(&mut bytes);
        return audio_data;
     } else {
         
     }
    "".to_string()
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_fs::init())
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![
            get_languages,
            get_translated,
            texttoaudio
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
