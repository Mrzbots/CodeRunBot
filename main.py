import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineQuery, InlineQueryResultArticle, InlineKeyboardMarkup, InlineKeyboardButton
from settings import *

logging.basicConfig(level=logging.INFO)

app = Client("piston_bot", api_id=123456, api_hash="your_api_hash")

@app.on_message(filters.command("help"))
async def help_message(client, message: Message):
    await message.reply(USAGE_MSG)

@app.on_message(filters.command("stats"))
async def stats_message(client, message: Message):
    # Get stats from database
    stats = await stats_collection.find_one()
    await message.reply(STATS_MSG.format(**stats))

@app.on_message(filters.command("run"))
async def run_message(client, message: Message):
    request, err = create_request(message.command_arguments())
    if err:
        await message.reply(USAGE_MSG)
        return

    response = await run_code(request)
    await message.reply(format_piston_response(request, response))
    if response.result != result_unknown:
        await message.reply(fork_button(request))

@app.on_message(filters.command("langs"))
async def langs_message(client, message: Message):
    languages, err = get_languages()
    if err:
        await message.reply(ERROR_STRING)
        return

    text_lines = []
    text_lines.append("<b>Supported languages:</b>")
    for lang in languages:
        text_lines.append(f"<pre>{html.escape(lang)}</pre>")
    await message.reply("\n".join(text_lines))

@app.on_inline_query()
async def inline_query(client, inline_query: InlineQuery):
    query_data = await run_inline_query(inline_query.query)
    await client.answer_inline_query(inline_query.id, [query_data])

async def run_inline_query(query: str) -> InlineQueryResultArticle:
    request, err = create_request(query)
    if err:
        return InlineQueryResultArticle(
            title="Bad Query",
            description=INLINE_USAGE_MSG_PLAINTEXT,
            message=INLINE_USAGE_MSG,
        )

    response = await run_code(request)
    message = format_piston_response(request, response)
    if response.result == result_success:
        return InlineQueryResultArticle(
            title="Output",
            description=response.output,
            message=message,
            reply_markup=fork_button(request),
        )
    elif response.result == result_error:
        return InlineQueryResultArticle(
            title="Error",
            description=response.output,
            message=message,
            reply_markup=fork_button(request),
        )
    else:
        return InlineQueryResultArticle(
            title="Error",
            description="Unknown error",
            message=message,
        )

async def create_request(text: str) -> Tuple[RunRequest, str]:
    lang, code = text.split(maxsplit=1)
    code = code.lstrip()
    stdin_match = re.search(r'\s\/stdin\b', code)
    if stdin_match:
        start, end = stdin_match.start(), stdin_match.end()
        code, stdin = code[:start], code[end + 1:]
    else:
        stdin = ""
    return RunRequest(lang, code, stdin), ""

async def format_piston_response(request: RunRequest, response: RunResponse) -> str:
    if response.result == result_unknown:
        return ERROR_STRING
    elif response.result == result_error:
        return build_output(
            {
                BlockLanguage: request.language,
                BlockCode: request.code,
                BlockStdin: request.stdin,
                BlockError: response.output,
            },
            request.language,
        )
    else:
        return build_output(
            {
                BlockLanguage: request.language,
                BlockCode: request.code,
                BlockStdin: request.stdin,
                BlockCompilerOutput: response.compiler_output,
                BlockOutput: response.output,
            },
            request.language,
        )

async def fork_button(request: RunRequest) -> InlineKeyboardMarkup:
    fork_text = request.language + "\n" + request.code
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Fork",
                    switch_inline_query_current_chat=fork_text,
                ),
            ],
        ],
    )
    return inline_keyboard

app.run()
