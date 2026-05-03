import asyncio
import re
from aiogram import Bot, Dispatcher, types, F

# ТВОЙ ТОКЕН (лучше взять у BotFather)
API_TOKEN = '8619730075:AAG0ycNyCUFv3qk4a-KEbMd4Eb3AWTx6300'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# База данных в памяти (сотрется при перезагрузке, если не прикрутить БД позже)
players = {}


# Твой словарь BUILDINGS
BUILDINGS = {"ферма": {"price": 300000, "income": 100000, "pop_bonus": 100000, "var": "farm"},
    "завод": {"price": 600000, "income": 250000, "var": "zavod"},
    "шахта": {"price": 500000, "income": 200000, "var": "minner"},
    "нефтевышка": {"price": 1000000, "income": 220000, "var": "neft"},
    "университет": {"price": 600000, "income": -50000, "research": 0.5, "var": "univers"},
    "кб": {"price": 500000, "income": -30000, "research": 0.25, "var": "patent"}, # используем patent для КБ
    "казармы": {"price": 300000, "income": -30000, "var": "armia"},
    "военный_завод": {"price": 900000, "income": -100000, "var": "war_zavod"},
    "порт": {"price": 600000, "income": 200000, "var": "port"},
    "верфь": {"price": 1200000, "income": -150000, "var": "verf"},
    "электростанция": {"price": 800000, "income": 200000, "var": "elektro"},
    "ратуша": {"price": 500000, "income": 100000, "tax_bonus": 0.05, "limit": 6, "var": "ratush"}, # 6 штук по 5% = 30%
    "укрепрайон": {"price": 1200000, "income": -100000, "var": "xz"},
    "жд_узел": {"price": 1200000, "income": 200000, "var": "r_z_d"},
    "госпиталь": {"price": 400000, "income": -20000, "var": "ochki"}, # просто заглушка
    "полиция": {"price": 500000, "income": -50000, "var": "licenz"} # просто заглушка
}

# --- ТУТ ВСЕ ТВОИ ФУНКЦИИ (register_country, build_logic, next_year_process, government_report) ---

# Создаем пустой словарь для всех игроков

# Так будет выглядеть структура для одного игрока:
# (user_id — это уникальный номер пользователя из Телеграма)

import re

@dp.message()
async def register_country(message: types.Message):
    # Проверяем, что это именно анкета
    if "#обновление" in message.text:
        text = message.text
        user_id = message.from_user.id
        
        # Если игрока еще нет в базе, создаем ему пустой профиль
        if user_id not in players:
            # Тут используй тот длинный словарь, который мы сделали раньше
            players[user_id] = {
    "money": 0,
    "money_in_year": 0,
    "money1": 0,  # доход с построек в год
    "money2": 0,  # расход построек в год
    "population": 0,  # население
    "population_in_year": 0,  # население в год
    "country_name": "",  # название страны (текст)
    "year": 0,
    "age": "",  # эпоха
    "polit_stroi": "",  # полит строй
    "migration": 0,  # эмигранты
    "capital": "",  # столица
    "admin_d": "",  # административное деление
    "avtonom": "",  # автономии/колонии
    "doroga": 0,  # дорожная сеть
    "help": 0,  # иностранная помощь
    "armia": 0,  # расходы на армию
    "dolg": 0,  # выплата долгов
    "gosdolg": 0,  # гос долг
    "hard_prom": 0,  # тяжелая промышленность
    "prod_bez": 0,  # продовольств.безопасность
    "export": [],  # список экспорта товаров
    "import": [],  # список покупок товаров
    "import_money": 0,  # доходы с продаж
    "farm": 0,
    "minner": 0,  # шахты
    "neft": 0,  # нефтевышки
    "zavod": 0,
    "war_zavod": 0,
    "elektro": 0,  # электростанции
    "univers": 0,
    "ratush": 0,  # ратуши
    "port": 0,
    "verf": 0,  # верфи
    "r_z_d": 0,  # жд узлы
    "kosmoport": 0,  # космопорты
    "ochki_in_year": 0,  # очки исследований в год
    "ochki": 0,  # накоплено очков
    "technolog": [],  # изученные технологии
    "licenz": [],  # лицензии
    "patent": [],  # свои патенты
    "soiznik": [],  # союзники
    "torg_partner": [],  # торговые партнеры
    "neitr": [],  # нейтральные страны
    "warg": [],  # враги
    "chlenstvo": [],  # членство в альянсах
    "xz": 0  # контрибуции и репарации
        # --- Новые поля из анкеты ---
    "flag": "",              # флаг страны (эмодзи или ссылка)
    "cities": [],            # крупные города (список)
    "polit_stroi": "",
    "ideology": "",          # идеология
    "pravlenie": "",         # тип правления
    "dynasty": "",           # династия
    "pravitel": "",          # имя правителя
    "religia": "",           # религия
    "valuta": "",            # валюта
    "territory_size": 0,     # размер территории (число)
    "language": "",          # язык
    "stability": "",         # стабильность (текст или число)
    "war_support": "",       # поддержка войны
    "peoples": [],           # народы (список)
    "profit": 0 #прибыль

}

        # Начинаем вытаскивать данные через поиск по тексту
        try:
            # Ищем текст между "Название — " и концом строки
            name_match = re.     search(r"Название — (.+)", text)
            if name_match:
                players[user_id]["country_name"] = name_match.group(1).strip()
                
        	capital_match = re.search(r"Столица — (.+)", text)
            if capital_match:
                players[user_id]["capital"] = capital_match.group(1).strip()
                
        	population_match = re.search(r"Население — (.+)", text)
            if population_match:
                players[user_id]["population"] = population_match.group(1).strip()
                
            cities_match = re.search(r"Крупные города — (.+)", text)
            if cities_match:
    # Берем строку, режем её по запятой и убираем лишние пробелы
    players[user_id]["cities"] = [c.strip() for c in cities_match.group(1).split(",")]
    
            ideology_match = re.search(r"Идеология — (.+)", text)
            if ideology_match:
                players[user_id]["ideology"] = ideology_match.group(1).strip()
                
             pravlenie_match = re.search(r"Тип правления — (.+)", text)
            if pravlenie_match:
                players[user_id]["pravlenie"] = pravlenie_match.group(1).strip()
            
                        # 7. Политический режим
            polit_regime_match = re.search(r"Политический режим — (.+)", text)
            if polit_regime_match:
                players[user_id]["polit_stroi"] = polit_regime_match.group(1).strip()

            # 8. Династия
            dynasty_match = re.search(r"Династия — (.+)", text)
            if dynasty_match:
                players[user_id]["dynasty"] = dynasty_match.group(1).strip()

            # 9. Население (вытягиваем только цифры)
            pop_match = re.search(r"Население — (.+)", text)
            if pop_match:
                # Убираем всё, кроме цифр, чтобы можно было считать налоги
                pop_digits = "".join(filter(str.isdigit, pop_match.group(1)))
                players[user_id]["population"] = int(pop_digits) if pop_digits else 0

            # 10. Правитель
            leader_match = re.search(r"Правитель — (.+)", text)
            if leader_match:
                players[user_id]["pravitel"] = leader_match.group(1).strip()

            # 11. Религия
            relig_match = re.search(r"Религия — (.+)", text)
            if relig_match:
                players[user_id]["religia"] = relig_match.group(1).strip()

            # 12. Валюта
            valuta_match = re.search(r"Валюта — (.+)", text)
            if valuta_match:
                players[user_id]["valuta"] = valuta_match.group(1).strip()

            # 13. Территория (площадь)
            terr_match = re.search(r"Территория — (.+)", text)
            if terr_match:
                # Оставляем только цифры (площадь в км2)
                terr_digits = "".join(filter(str.isdigit, terr_match.group(1)))
                players[user_id]["territory_size"] = int(terr_digits) if terr_digits else 0

            # 14. Язык
            lang_match = re.search(r"Язык — (.+)", text)
            if lang_match:
                players[user_id]["language"] = lang_match.group(1).strip()

            # 15. Стабильность
            stab_match = re.search(r"Стабильность — (.+)", text)
            if stab_match:
                players[user_id]["stability"] = stab_match.group(1).strip()

            # 16. Поддержка войны
            war_sup_match = re.search(r"Поддержка войны — (.+)", text)
            if war_sup_match:
                players[user_id]["war_support"] = war_sup_match.group(1).strip()

            # 17. Народы (делаем списком через запятую)
            peoples_match = re.search(r"Народы — (.+)", text)
            if peoples_match:
                players[user_id]["peoples"] = [p.strip() for p in peoples_match.group(1).split(",")]
                
def calculate_yearly_income(user_id):
    p = players[user_id]
    
    # Считаем бонус ратуш: каждая дает +5% к налогам (макс 30 штук)
    count_ratush = p.get("ratush", 0)
    if count_ratush > 30: count_ratush = 30
    
    tax_multiplier = 1 + (count_ratush * 0.05)
    
    # Налог: население * множитель ратуш
    total_tax = p["population"] * tax_multiplier
    
    # Прибыль = Налоги + Доход с построек - Расходы
    profit = total_tax + p["money1"] - p["money2"]
    return int(profit)


@dp.message()
async def build_logic(message: types.Message):
    # Команда должна быть: Построить ферма 5
    if message.text.lower().startswith("построить"):
        user_id = message.from_user.id
        parts = message.text.split()
        
        # 1. Базовая проверка игрока
        if user_id not in players:
            return await message.answer("❌ Сначала зарегистрируй страну (пришли анкету)!")

        try:
            # Разбираем сообщение
            name = parts[1].lower() # название здания
            amount = int(parts[2])  # количество
            
            if amount <= 0:
                return await message.answer("❌ Количество должно быть больше 0.")

            # 2. Проверяем, есть ли такое здание в прайс-листе
            if name not in BUILDINGS:
                return await message.answer(f"❌ Здания '{name}' не существует в списке.")

            b_data = BUILDINGS[name]
            total_cost = b_data["price"] * amount
            var_name = b_data["var"] # переменная в словаре игрока (zavod, farm и т.д.)

            # 3. ПРОВЕРКА ЛИМИТА (для Ратуши)
            if "limit" in b_data:
                current_count = players[user_id].get(var_name, 0)
                if current_count + amount > b_data["limit"]:
                    can_build = b_data["limit"] - current_count
                    return await message.answer(f"❌ Лимит зданий '{name}' достигнут. Можно построить еще: {max(0, can_build)}")

            # 4. ПРОВЕРКА ДЕНЕГ
            if players[user_id]["money"] < total_cost:
                return await message.answer(f"❌ Недостаточно средств! Нужно: ${total_cost}, в казне: ${players[user_id]['money']}")

            # 5. ПРОЦЕСС СТРОИТЕЛЬСТВА
            # Списываем деньги сразу всей суммой
            players[user_id]["money"] -= total_cost
            
            # Добавляем количество зданий в переменную игрока
            players[user_id][var_name] = players[user_id].get(var_name, 0) + amount
            
            # Настраиваем ежегодный доход (money1) и расходы
            # Мы прибавляем доход сразу за все построенные здания
            players[user_id]["money1"] += b_data["income"] * amount
            
            # Если здание дает бонус к приросту населения (как ферма)
            if "pop_bonus" in b_data:
                players[user_id]["population_in_year"] += b_data["pop_bonus"] * amount

            # 6. ИТОГОВЫЙ ОТВЕТ
            await message.answer(
                f"✅ Строительство завершено!\n"
                f"🏗 Объект: {name.capitalize()}\n"
                f"🔢 Количество: {amount} шт.\n"
                f"💸 Списано: ${total_cost}\n"
                f"📊 Текущий доход в год: ${players[user_id]['money1']}"
            )

        except (IndexError, ValueError):
            await message.answer("❌ Ошибка формата! Пиши: Построить [название] [количество]\nПример: Построить завод 2")

@dp.message(F.text.lower().in_(["/справка", "справка", "гос справка"]))
async def government_report(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in players:
        return await message.answer("❌ У вас еще нет государства. Пришлите анкету!")

    p = players[user_id]
    
    # --- 1. Считаем бюджетные показатели ---
    # Считаем бонус ратуш
    count_ratush = p.get("ratush", 0)
    tax_multiplier = 1 + (min(count_ratush, 6) * 0.05)
    
    # Налоги (население * 1 монета * бонус ратуш)
    taxes = int(p["population"] * 1 * tax_multiplier)
    
    # Доходы и расходы от зданий (мы их уже храним в money1)
    # Если ты хочешь разделить их в справке, можно считать на лету
    total_income = taxes + p["money1"]
    
    # --- 2. Формируем текст справки ---
    report = (
        f"📊 **ГОСУДАРСТВЕННАЯ СПРАВКА: {p['country_name']}** {p.get('flag', '')}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👑 **Правитель:** {p.get('pravitel', 'Неизвестно')}\n"
        f"📅 **Год:** {p['year']}-й ({p.get('age', 'Эпоха не задана')})\n"
        f"👥 **Население:** {p['population']:,} чел. (+{p.get('population_in_year', 0):,} в год)\n"
        f"🏛 **Полит. строй:** {p.get('polit_stroi', 'Не задан')}\n"
        f"📜 **Стабильность:** {p.get('stability', 'Норма')}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 **ЭКОНОМИКА И БЮДЖЕТ**\n"
        f"💵 **В казне:** {p['money']:,} $\n"
        f"📈 **Доход (налоги):** +{taxes:,} $\n"
        f"🏭 **Доход (пром.):** {p['money1']:,} $\n"
        f"💸 **Чистая прибыль в год:** {total_income:,} $\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🏗 **ИНФРАСТРУКТУРА**\n"
        f"🏘 Ратуши: {p.get('ratush', 0)}/6 | 🚜 Фермы: {p.get('farm', 0)}\n"
        f"🏭 Заводы: {p.get('zavod', 0)} | ⛏ Шахты: {p.get('minner', 0)}\n"
        f"🎓 Универы: {p.get('univers', 0)} | 🧪 Очки иссл.: {p.get('ochki', 0):.1f}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🤝 **ПОЛИТИЧЕСКИЕ ОТНОШЕНИЯ**\n"
        f"⚔️ Враги: {', '.join(p.get('warg', [])) if p.get('warg') else 'Нет'}\n"
        f"🛡 Союзники: {', '.join(p.get('soiznik', [])) if p.get('soiznik') else 'Нет'}\n"
        f"🤝 Партнеры: {len(p.get('torg_partner', []))} стран\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🚩 *Используйте #обновление для изменения данных*"
    )

    await message.answer(report, parse_mode="Markdown")

@dp.message(F.text.lower().in_(["/next_year", "следующий год", "год"]))
async def next_year_process(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in players:
        return await message.answer("❌ Сначала создайте страну!")

    p = players[user_id]

    try:
        # --- 1. РАСЧЕТ ДОХОДОВ ---
        # Бонус ратуш (5% за каждую, макс 30%)
        count_ratush = p.get("ratush", 0)
        tax_multiplier = 1 + (min(count_ratush, 6) * 0.05)
        
        # Налоги с населения
        taxes = int(p["population"] * 1 * tax_multiplier)
        
        # Доход с построек (уже хранится в money1 как разница доходов и расходов)
        buildings_profit = p["money1"]
        
        # Итоговая чистая прибыль за год
        yearly_profit = taxes + buildings_profit

        # --- 2. ОБНОВЛЕНИЕ ПАРАМЕТРОВ ---
        # Прибавляем прибыль в казну
        p["money"] += yearly_profit
        
        # Прирост населения (базовый + от ферм)
        # Если в population_in_year мы записывали бонус от ферм
        p["population"] += p.get("population_in_year", 0)
        
        # Очки исследований (Университеты и КБ)
        research_gain = (p.get("univers", 0) * 0.5) + (p.get("patent", 0) * 0.25)
        p["ochki"] += research_gain
        
        # Увеличиваем счетчик года
        p["year"] += 1

        # --- 3. ОТВЕТ ИГРОКУ ---
        response = (
            f"🔔 **ОТЧЕТ ЗА {p['year']-1}-й ГОД**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 **Налоги:** +{taxes:,} $\n"
            f"🏭 **Доход производств:** {buildings_profit:,} $\n"
            f"📈 **Чистая прибыль:** +{yearly_profit:,} $\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👥 **Прирост населения:** +{p.get('population_in_year', 0):,} чел.\n"
            f"🧪 **Получено очков науки:** +{research_gain}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🏦 **Итого в казне:** {p['money']:,} $\n"
            f"📅 **Наступил {p['year']}-й год!**"
        )
        
        await message.answer(response, parse_mode="Markdown")

    except Exception as e:
        await message.answer(f"❌ Ошибка при расчете года: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
 	
