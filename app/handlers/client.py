import html
import logging
import re

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.config import config
from app.db.requests import add_lead
from app.handlers.states import LeadForm
from app.keyboards.keyboards import cancel_kb, phone_request_kb, remove_kb, start_kb

logger = logging.getLogger(__name__)

router = Router()

PHONE_RE = re.compile(r"^\+?\d[\d\s\-()]{6,20}$")


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "👋 Здравствуйте! Я бот для приёма заявок.\n\n"
        "Нажмите кнопку ниже, чтобы оставить заявку, и мы свяжемся с вами в течение часа.",
        reply_markup=start_kb,
    )


@router.callback_query(F.data == "start_lead")
async def start_lead(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(LeadForm.name)
    await callback.message.edit_text("Введите ваше имя:", reply_markup=cancel_kb)
    await callback.answer()


@router.callback_query(F.data == "cancel")
async def cancel_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text("Заявка отменена.")
    await callback.message.answer("Чтобы начать заново, нажмите /start", reply_markup=remove_kb)
    await callback.answer()


@router.message(LeadForm.name)
async def process_name(message: Message, state: FSMContext) -> None:
    if not message.text or len(message.text.strip()) < 2:
        await message.answer("Пожалуйста, введите корректное имя.", reply_markup=cancel_kb)
        return
    await state.update_data(name=message.text.strip())
    await state.set_state(LeadForm.phone)
    await message.answer(
        "Укажите ваш номер телефона (или отправьте контакт кнопкой ниже):",
        reply_markup=phone_request_kb(),
    )


@router.message(LeadForm.phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext) -> None:
    await state.update_data(phone=message.contact.phone_number)
    await state.set_state(LeadForm.description)
    await message.answer(
        "Опишите вашу задачу или вопрос:",
        reply_markup=cancel_kb,
    )


@router.message(LeadForm.phone, F.text)
async def process_phone_text(message: Message, state: FSMContext) -> None:
    phone = message.text.strip()
    if not PHONE_RE.match(phone):
        await message.answer(
            "Похоже, номер указан неверно. Попробуйте ещё раз или отправьте контакт кнопкой.",
            reply_markup=phone_request_kb(),
        )
        return
    await state.update_data(phone=phone)
    await state.set_state(LeadForm.description)
    await message.answer(
        "Опишите вашу задачу или вопрос:",
        reply_markup=cancel_kb,
    )


@router.message(LeadForm.description)
async def process_description(message: Message, state: FSMContext) -> None:
    if not message.text or len(message.text.strip()) < 3:
        await message.answer("Пожалуйста, опишите задачу текстом.", reply_markup=cancel_kb)
        return

    data = await state.get_data()
    name = data["name"]
    phone = data["phone"]
    description = message.text.strip()

    lead = await add_lead(
        user_id=message.from_user.id,
        username=message.from_user.username,
        name=name,
        phone=phone,
        description=description,
    )

    await state.clear()
    await message.answer(
        "✅ Спасибо! Мы свяжемся с вами в течение часа.",
        reply_markup=remove_kb,
    )

    admin_text = (
        "🆕 Новая заявка #{id}\n\n"
        "👤 Имя: {name}\n"
        "📱 Телефон: {phone}\n"
        "💬 Описание: {description}\n\n"
        "Telegram: @{username} (id: {user_id})"
    ).format(
        id=lead.id,
        name=html.escape(name),
        phone=html.escape(phone),
        description=html.escape(description),
        username=html.escape(message.from_user.username or "—"),
        user_id=message.from_user.id,
    )
    for admin_id in config.admin_ids:
        try:
            await message.bot.send_message(admin_id, admin_text)
        except Exception:
            logger.exception(
                "Failed to notify admin %s about lead #%s", admin_id, lead.id
            )
