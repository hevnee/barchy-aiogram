# barchy aiogram

## Table of Contents

* [About](#about)
* [Usage](#usage)

## About

[barchy](https://t.me/barchy_bot) is a telegram bot with AI part, working on [aiogram](https://github.com/aiogram/aiogram/). <br/>
barchy uses [LibreTranslate](https://libretranslate.com/) for translate.

## Usage

1. Install all libraries from the requirements.txt.
2. Rename `TOKEN` from `bot/configs/settings.py` to your token.
3. For the AI to work, you must download [LibreTranslate repository from github](https://github.com/LibreTranslate/LibreTranslate/) and [libretranslate on PyPI](https://pypi.org/project/libretranslate/).
4. Rename `MODEL_NAME` from `bot/services/generator.py` to the model from `models.md` and you can also rename it to another model you know.
5. Run libretranslate.
6. Run `run.bat`.
7. Enjoy!