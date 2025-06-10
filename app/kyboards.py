from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_cat, get_cat_Item

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Регистрация')],
                                     [KeyboardButton(text='Битва')],
                                     [KeyboardButton(text='oi oi oi'),
                                      KeyboardButton(text='Фурри')],
                                     [KeyboardButton(text='Магазин Субарика')],
                                     [KeyboardButton(text='Листинг хомяка')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выбри пж')

war = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Hamster Combat', callback_data='Sigma')],
                                            [InlineKeyboardButton(text='чозабрето', callback_data='poop')]])


#IDphoto = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=f'{1}')]])# for i in range(1, phId + 1))
num = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Дать номер",
                                                    request_contact=True)]],
                          resize_keyboard=True)

async def categories():
    all_cat = await get_cat()
    keybord = InlineKeyboardBuilder()
    for cat in all_cat:
        keybord.add(InlineKeyboardButton(text=cat.name, callback_data=f"category_{cat.id}"))
    keybord.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keybord.adjust(2).as_markup()

async def items(category_id):
    all_items = await get_cat_Item(category_id)
    keybord = InlineKeyboardBuilder()
    for item in all_items:
        keybord.add(InlineKeyboardButton(text=item.name, callback_data=f"item_{item.id}"))
    keybord.add(InlineKeyboardButton(text='К категориям', callback_data='to_cats'))
    return keybord.adjust(2).as_markup()

home2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='На главную', callback_data='to_main'),
                                              InlineKeyboardButton(text='К категориям', callback_data='to_cats')]])

def webapp_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Добивай изгоя!!!", web_app=WebAppInfo(
            url='...'
        )
    )
