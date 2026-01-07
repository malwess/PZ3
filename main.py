class CipherDescriptor:

    def __init__(self, cipher_type='caesar', shift=3):
        self.cipher_type = cipher_type  # 'caesar' или 'atbash'
        self.shift = shift  # сдвиг для Цезаря
        self.data = {}  # хранилище

    def __get__(self, obj, objtype=None):
        #Возвращает зашифрованный текст для объекта
        if obj is None:
            return self
        return self.data.get(id(obj), '')

    def __set__(self, obj, value):
        #Присваивание текста -> автоматическое шифрование
        if not isinstance(value, str):
            raise ValueError("Значение должно быть строкой")

        if self.cipher_type == 'caesar':
            self.data[id(obj)] = self._caesar_cipher(value, self.shift)
        elif self.cipher_type == 'atbash':
            self.data[id(obj)] = self._atbash_cipher(value)
        else:
            raise ValueError(f"Неизвестный тип шифра: {self.cipher_type}")

    def _caesar_cipher(self, text, shift, decrypt=False):
        # Шифр Цезаря
        result = []

        for char in text:
            if char.isalpha():
                # Русский алфавит (с буквой ё)
                if 'а' <= char.lower() <= 'я' or char.lower() == 'ё':
                    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
                    is_upper = char.isupper()
                    char_lower = char.lower()

                    if decrypt:
                        # Дешифровка: сдвиг назад
                        index = (alphabet.index(char_lower) - shift) % len(alphabet)
                    else:
                        # Шифровка: сдвиг вперед
                        index = (alphabet.index(char_lower) + shift) % len(alphabet)

                    new_char = alphabet[index]
                    result.append(new_char.upper() if is_upper else new_char)

                # Английский алфавит
                elif 'a' <= char.lower() <= 'z':
                    alphabet = 'abcdefghijklmnopqrstuvwxyz'
                    is_upper = char.isupper()
                    char_lower = char.lower()

                    if decrypt:
                        index = (alphabet.index(char_lower) - shift) % len(alphabet)
                    else:
                        index = (alphabet.index(char_lower) + shift) % len(alphabet)

                    new_char = alphabet[index]
                    result.append(new_char.upper() if is_upper else new_char)
                else:
                    result.append(char)
            else:
                # Не буквенные символы
                result.append(char)

        return ''.join(result)

    def _atbash_cipher(self, text):
        # Шифр Атбаш
        result = []

        # Алфавиты
        ru_lower = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        ru_upper = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        en_lower = 'abcdefghijklmnopqrstuvwxyz'
        en_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        # Перевернутые алфавиты
        ru_rev_lower = ru_lower[::-1]
        ru_rev_upper = ru_upper[::-1]
        en_rev_lower = en_lower[::-1]
        en_rev_upper = en_upper[::-1]

        for char in text:
            # Определяем к какому алфавиту принадлежит символ
            if 'а' <= char <= 'я':
                index = ru_lower.index(char)
                result.append(ru_rev_lower[index])
            elif 'А' <= char <= 'Я' or char == 'Ё':
                if char == 'Ё':
                    index = ru_upper.index('Ё')
                else:
                    index = ru_upper.index(char)
                result.append(ru_rev_upper[index])
            elif 'a' <= char <= 'z':
                index = en_lower.index(char)
                result.append(en_rev_lower[index])
            elif 'A' <= char <= 'Z':
                index = en_upper.index(char)
                result.append(en_rev_upper[index])
            else:
                # Не буквенные символы остаются без изменений
                result.append(char)

        return ''.join(result)


class Message:
    #Класс для работы с сообщениями.

    # Дескрипторы как атрибуты класса
    caesar_encrypted = CipherDescriptor(cipher_type='caesar', shift=3)
    atbash_encrypted = CipherDescriptor(cipher_type='atbash')

    def __init__(self, text=""):
        self._original_text = text  # Оригинальный текст

        # Присваивание через дескрипторы -> автоматическое шифрование
        self.caesar_encrypted = text
        self.atbash_encrypted = text

    @property
    def original_text(self):
        #Свойство для доступа к оригинальному тексту
        return self._original_text

    @original_text.setter
    def original_text(self, value):
        #При изменении текста автоматически обновляются шифрованные версии
        self._original_text = value
        self.caesar_encrypted = value  # Вызовет __set__ дескриптора
        self.atbash_encrypted = value  # Вызовет __set__ дескриптора

    def decrypt_caesar(self, shift=None):
        #Дешифровка текста, зашифрованного шифром Цезаря
        if shift is None:
            shift = 3  # Используем сдвиг по умолчанию

        cipher = CipherDescriptor(cipher_type='caesar', shift=shift)
        return cipher._caesar_cipher(self.caesar_encrypted, shift, decrypt=True)

    def decrypt_atbash(self):
        #Дешифровка текста, зашифрованного шифром Атбаш
        # Атбаш симметричен - шифрование = дешифрование
        cipher = CipherDescriptor(cipher_type='atbash')
        return cipher._atbash_cipher(self.atbash_encrypted)


# Пример использования
if __name__ == "__main__":
    # Создаем сообщение
    message = Message("Привет, Hello!")

    print("Оригинал:", message.original_text)
    print("Цезарь (зашифровано):", message.caesar_encrypted)
    print("Атбаш (зашифровано):", message.atbash_encrypted)
    print("Цезарь (расшифровано):", message.decrypt_caesar())
    print("Атбаш (расшифровано):", message.decrypt_atbash())

    # Изменяем текст
    message.original_text = "Новый текст"
    print("\nПосле изменения:")
    print("Цезарь:", message.caesar_encrypted)
    print("Расшифровка:", message.decrypt_caesar())