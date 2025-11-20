from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.repositories.requests import create_request
from app.services.openai_service import get_response, parse_request_with_ai
from app.services.requests_service import is_request_intent

router = Router()

class RequestFlow(StatesGroup):
    waiting_request = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    return message.answer("Привіт! Можу відповісти на питання або створити заявку.")


@router.message(StateFilter(None))
async def detect_intent(message: Message, state: FSMContext):
    text = message.text.lower()

    if is_request_intent(text):
        await message.answer(
            "Напишіть одним повідомленням:\n"
            "Cуть проблеми / питання\n"
            "Контакт для звʼязку (телефон, email, @telegram)\n\n"
            "Наприклад:\n"
            "«Не працює оплата на сайті, картка не проходить. "
            "@username або 0991234567»"
        )
        await state.set_state(RequestFlow.waiting_request)
        return

    answer = await get_response(message.text)
    return await message.answer(answer)


@router.message(StateFilter(RequestFlow.waiting_request))
async def handle_request(message: Message, state: FSMContext):
    text = message.text

    await message.answer("Формую заявку, зачекайте…")

    try:
        ai_data = await parse_request_with_ai(text)

        request_obj = await create_request(
            user_id=message.from_user.id,
            username=message.from_user.username,
            data=ai_data,
        )

    except Exception as e:
        await message.answer(f"Помилка при створенні заявки {e}")
        await state.clear()
        return

    await state.clear()

    await message.answer(
        "Заявка створена \n"
        f"ID: {request_obj.id}\n"
        f"Тема: {request_obj.title}"
    )
