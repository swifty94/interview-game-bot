---
**Interview Game Bot** – ваш ідеальний бот для гри "Інтерв'юер та Гість". Легкий запуск, зручне меню кнопок та покращене логування.
---

## 📋 **Що нового?**

1. **🛠️ Спрощений запуск**
 Тепер бот запускається однією командою:
 ```bash
 python .
 ```

2. **🎲 Визначення ролей**
 Киньте кубики, щоб випадково обрати **інтерв'юера** та **гостя**.

3. **📝 Генерація питань**
 Отримайте 10 унікальних питань у категоріях:
 - ⚡ **Бліц**
 - 📚 **Нормал**

4. **🔄 Зручне меню кнопок**
 Усі команди доступні через інтерактивне меню:
 - **Отримати питання**
 - **Додати питання**
 - **Бліц**
 - **Нормал**
 - **Кинути кубики**

5. **🔍 Покращене логування**
 SQL-запити та команди користувачів детально логуються.

---

## 🚀 **Запуск бота**

1. **Налаштуйте середовище**:
 ```bash
 pip install -r requirements.txt
 ```

2. **Запустіть бота**:
 ```bash
 python .
 ```

3. **Керуйте через меню** або використовуйте команди:

---

## 🧩 **Команди**

| **Команда** | **Опис** |
|-------------------------|-------------------------------------------|
| **/start**| Запускає бота та відображає головне меню. |
| **/question** | Генерує 10 унікальних запитань. |
| **/category <normal|blitz>** | Змінює категорію питань. |
| **/add_question <текст>** | Додає запитання до поточної категорії.|
| **/set_roles**| Визначає ролі "Інтерв'юер" і "Гість". |

---

## 🎨 **Скріншоти**

1. **Головне меню**
 ![Меню](img/menu.png)

2. **Визначення ролей**
 ![Кинути кубики](img/players.png)

3. **Генерація запитань**
 ![Запитання](img/questions.png)

4. **Перемикання категорій**
 ![Перемикання категорій](img/switch_question_type.png)

---

## 🧪 **Тестування**

Запуск усіх тестів:
```bash
python -m unittest discover -s tests -v
```

**Тести включають**:
1. **Генерацію 10 унікальних запитань**
2. **Логування SQL-запитів**
3. **Перевірку команд кнопок**
4. **Визначення ролей (кубики)**

---

**Interview Game Bot** – грайте, вчіться та насолоджуйтесь розмовами! 🎉

---