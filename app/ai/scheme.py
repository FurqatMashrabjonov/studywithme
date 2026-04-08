from pydantic import BaseModel, Field
from typing import List, Dict, Literal

class AgentResponse(BaseModel):
    text: str
    token: object



# Tool models
from pydantic import BaseModel, Field
from typing import List, Dict, Literal

class Flashcard(BaseModel):
    question: str = Field(
        description="Flashcardning oldi tomonida ko'rsatiladi. Asosiy tushuncha, atama yoki qisqa savol. "
                    "Foydalanuvchi ushbu savolga javob topish uchun o'ylashi kerak."
    )
    answer: str = Field(
        description="Flashcardning orqa tomonida ko'rsatiladi. Savolga to'liq va aniq javob yoki tushuntirish. "
                    "Misollar, ta'riflar va muhim detalllarni o'z ichiga olishi mumkin."
    )

class FlashcardWrapper(BaseModel):
    title: str = Field(
        description="Flashcard to'plamining aniq va chuqur sarlavhasi. "
                    "Sarlavha mavzunining mazmunini to'liq aks ettirishi kerak va foydalanuvchiga darhol "
                    "qaysi mavzu bo'yicha flashcard yaratilganini tushuntirishi kerak. "
                    "Masalan: 'Python Asoslari: O'zgaruvchilar, Ma'lumot Turlari va Operatorlar' yoki "
                    "'Biologija: Hujayraning Strukturasi va Uning Funksiyalari'."
    )
    cards: List[Flashcard] = Field(
        description="Flashcardlarning ro'yxati. Har bir flashcard bir tushunchani o'rganishga mo'ljallangan."
    )

class QuizQuestion(BaseModel):
    question: str = Field(
        description="Test savoli matni. Aniq, tushunarli va bir qiymatli bo'lishi kerak. "
                    "Savol foydalanuvchiga to'g'ri javobni tanlashga undaydigan qilib tuzilishi kerak."
    )
    options: Dict[str, str] = Field(
        description="To'g'ri javob variantlari lug'ati. "
                    "Kalitlar faqat quyidagilardan iborat bo'lishi kerak: 'a', 'b', 'c', 'd'. "
                    "Qiymatlar - javob variantlarining to'liq matni. "
                    "Masalan: {'a': 'Birinchi variant', 'b': 'Ikkinchi variant', 'c': 'Uchinchi variant', 'd': 'To'rtinchi variant'}"
    )
    correct_option: Literal['A', 'B', 'C', 'D'] = Field(
        description="To'g'ri javobning identifikatori. "
                    "Faqat bitta katta lotin harfi bo'lishi shart: 'A', 'B', 'C' yoki 'D'. "
                    "Bu qiymat options lug'atidagi kalitlarning katta harfiga mos kelishi kerak."
    )
    explanation: str = Field(
        description="Nega aynan shu javob to'g'ri ekanligi haqida batafsil izoh. "
                    "Xato variantlarning nima uchun noto'g'ri ekanligini tushuntirish mumkin. "
                    "Izoh qisqa bo'lsa-da, ilmiy asoslangan va foydalanuvchini o'rgatuvchi bo'lishi kerak."
    )

class QuizWrapper(BaseModel):
    title: str = Field(
        description="Test to'plamining aniq va chuqur sarlavhasi. "
                    "Sarlavha testning mavzusini, qo'llanadigan bilim darajasini va muhim tushunchalarni "
                    "to'liq aks ettirishi kerak. Foydalanuvchi sarlavhani o'qiganda, "
                    "qaysi soha va qaysi darajadagi bilimni sinab ko'rishi kerakligini tushuniishi kerak. "
                    "Masalan: 'Matematika: Chiziqli Tenglamalar va Ularning Tizimlari (O'rta Daraja)' yoki "
                    "'Ingliz Tili: Past Tense Grammatikasi va Amaliy Qo'llanish'."
    )
    questions: List[QuizQuestion] = Field(
        description="Test savollari ro'yxati. Har bir savol mustaqil tushunchani tekshiradi. "
                    "Savol-javoblar testning sarlavhasidagi mavzuning turli tomonlarini qamrab olishi kerak."
    )

class ImageGenerationPrompt(BaseModel):
    prompt: str = Field(
        description="Rasm generatsiya qilish uchun AI modeliga beriladi. "
    )
