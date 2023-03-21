from aiogram.types import ReplyKeyboardMarkup,  KeyboardButton

btnMain = KeyboardButton('🏠 Главное меню')
#btnBack = KeyboardButton('↩️ Назад')

# --- Main menu ---
btnWorkout = KeyboardButton('💪 Тренировки')
btnOther = KeyboardButton('🚸 Другое')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnWorkout, btnOther)

# --- Workout menu ---
btnPushups = KeyboardButton('🥇 200 pushups')
btnSitups = KeyboardButton('🥈 200 crunches')
btnPlank = KeyboardButton('🥉 10 minute planka')
workoutMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnPushups, btnSitups, btnPlank, btnMain)

# --- Train menu ---
btnStartTrain = KeyboardButton('🫡 Начать тренировку')
btnHistoryTrain = KeyboardButton('📊 История тренировок')
curtrainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnStartTrain, btnHistoryTrain, btnMain)

# --- Other menu ---
btnInfo = KeyboardButton('💡 Информация')
otherMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnInfo, btnMain)