from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command


import app.kyboards as kb
import app.database.requests as rq

from aiogram.fsm .context import FSMContext
from app.State import Register, Buy_ak

router = Router()

@router.message(CommandStart()) # ответ на /start
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id, message.from_user.username)
    await message.answer(f"Привет {message.from_user.first_name}", reply_markup=kb.main)
    print(message.from_user.username)


'''@router.message(F.text == '1488')
async def poshalka(message: Message):
    await message.reply('ОООООО ПОСХАЛКО ВКЛЮЧАЕМ ВЕНТИЛЯТОРИ 1488')
    print(message)
'''
@router.message(F.text == 'Топ инвесторов') #ответ на кнопку Битва
async def sigma(message: Message):
    await message.answer('Выберай с умом')

'''@router.message(F.text == 'получить фото') #неработает
async def sigma(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAIBeWa1HC76ygQsJHScHhgls92NLfJIAAJY1jEbrPOYST-BxuwFoC-wAQADAgADeQADNQQ')
'''
'''@router.callback_query(F.data == 'Sigma') #ответ на Хомячки
async def echkeria(callback: CallbackQuery):
    await callback.answer('Харош')
    await callback.message.answer('хомячки побежали на листинг')

@router.callback_query(F.data == 'poop')
async def ponos(callback: CallbackQuery):
    await callback.answer('ыыыыыы 52')
    await callback.message.answer('вот это смефняфка')'''

'''@router.message(F.text == 'oi oi oi')
async def oioioi(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAMxZjIv0kmPaHtE8aDQVBfSRdD9UgEAAp7hMRuZw5hJezXiosauTyQBAAMCAAN5AAM0BA')
'''
'''@router.message(F.text == 'Алан')
async def Alan(message: Message):
    print('yes')
    await message.answer_photo(photo=str(photoID[-1]))'''

'''@router.message(F.text == 'Фурри')
async def oioioi(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAOxaEiEcRO-1xfx1TI_mjCO0qxCoHcAAp7yMRtLPklKxjwNmoSgdW0BAAMCAAN5AAM2BA')
    await message.answer('...')'''

# @router.message(F.text == 'ID фото')
# async def IDphoto(message: Message):
#     await message.answer(reply_markup=kb.IDphoto)

photoID = []
photoID_len = len(photoID)

@router.message(F.photo, Command('фото'))
async def photo(message: Message):
    photo_data = message.photo[-1]
    photoID.append(photo_data.file_id)
    await message.answer('Фото загружено')
    print(photoID[-1])

@router.message(F.text == 'Регистрация')
async def register(mes:Message, state:FSMContext):
    await state.set_state(Register.name)
    await mes.answer('Введите ваше имя')

@router.message(Register.name)
async def reg_name(mes:Message,state:FSMContext):
    await state.update_data(name=mes.text)
    await state.set_state((Register.number))
    await mes.answer("Номер?", reply_markup=kb.num)

@router.message(Register.number)
async def reg_name(mes:Message,state:FSMContext):
    await state.update_data(number=mes.contact.phone_number)
    await state.update_data(nicname=mes.from_user.username)
    data = await state.get_data()
    await mes.answer(f'Имя: {data["name"]}\nНомер: {data["number"]}', reply_markup=kb.main)
    print(f'Имя: {data["nicname"]}\nНомер: +{data["number"]}')
    await rq.set_num(data["number"], data["name"], mes.from_user.username)
    await state.clear()

@router.message(F.text == 'Акции')
async def catolog(mes:Message):
    await mes.answer('Выбери категорию', reply_markup=await kb.categories())

@router.callback_query(F.data.startswith('category_'))
async def category_item(callback:CallbackQuery):
    await callback.message.delete()
    await callback.answer('Ты выбрал категорию')
    await callback.message.answer('Выбери предмет', reply_markup=await kb.items(callback.data.split('_')[1]))

@router.callback_query(F.data.startswith('item_'))
async def category_item(callback:CallbackQuery, state:FSMContext):
    item_data = await rq.get_item(callback.data.split('_')[1])
    await callback.message.delete()
    await callback.answer('Ты выбрал предмет')
    await callback.message.answer(f'Название: {item_data.name}\nОписание: {item_data.description}\nЦена: {item_data.prise}₽', reply_markup=await kb.buy_sell(item_data.id))

@router.callback_query(F.data == 'to_main')
async def home(callback:CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Спасибо что выбрал меня')

@router.callback_query(F.data == 'to_cats')
async def home(callback:CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Выбери категорию', reply_markup=await kb.categories())

@router.callback_query(F.data.startswith('buy_'))
async def buy_ak(cb:CallbackQuery, state:FSMContext):
    item = await rq.get_item(cb.data.split('_')[1])
    await state.set_state(Buy_ak.ak)
    await state.update_data(ak=item.name, id=item.id)
    await cb.message.delete()
    await state.set_state(Buy_ak.count)
    await cb.message.answer('Введите кол-во акций которые вы хотите купить')

@router.message(Buy_ak.count)
async def count_ak(mes:Message, state:FSMContext):
    await state.update_data(count=mes.text)
    data = await state.get_data()
    item = await rq.get_item(data["id"])
    user = await rq.get_user(mes.from_user.id)
    if user.count_money != -1:
        if int(data["count"]) <= item.count and int(data["count"]) * int(item.prise) <= int(user.count_money):
            await mes.answer(text=f'Вы купили: {data["ak"]}\nВ размере: {data["count"]}')
            await rq.update_user(user.tg_id, int(data["count"]) * int(item.prise))
            await rq.update_item(item.id, data["count"])
            await state.clear()
        elif int(data["count"]) <= item.count and int(data["count"]) * int(item.prise) > int(user.count_money):
            await mes.answer(text=f'У вас не хватает денег на балансе\nВаш баланс: {user.count_money}\nВведите новое количество')
            await state.set_state(Buy_ak.count)
        elif int(data["count"]) > item.count and int(data["count"]) * int(item.prise) <= int(user.count_money):
            await mes.answer(text=f'Вы хотите купить слишком много акций\nТекущее количество акций: {item.count}\nВведите новое количество')
            await state.set_state(Buy_ak.count)
        else:
            await mes.answer(text=f'У вас не хватает денег на балансе и вы хотите купить слишком много акций\nВаш баланс: {user.count_money}\nТекущее количество акций: {item.count}\nВведите новое количество')
            await state.set_state(Buy_ak.count)
    else:
        await mes.answer(text='Вы не зарегистрированы')


'''@router.message(F.text == 'Листинг хомяка')
async def hamster(mes:Message):
    await mes.answer(
        'Добивай изгоя!!!',
        reply_markup= await kb.webapp_builder()
    )'''
