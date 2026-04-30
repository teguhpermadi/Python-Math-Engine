import httpx
import random
import logging
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)

class AIStoryteller:
    """
    Service untuk generate soal cerita menggunakan LM Studio (OpenAI Compatible).
    """
    def __init__(self, base_url: str = settings.LM_STUDIO_URL):
        self.base_url = base_url.rstrip('/')
        self.api_url = f"{self.base_url}/chat/completions"

    async def generate_story(
        self, 
        expression: str, 
        result: str, 
        operation: str, 
        theme: str = "general",
        rng: random.Random = None
    ) -> str:
        """
        Memanggil LM Studio untuk membuat soal cerita.
        """
        if rng is None:
            rng = random.Random()

        # Prompt engineering
        system_prompt = (
            "Anda adalah asisten pembuat soal matematika untuk siswa SD/SMP. "
            "Tugas Anda adalah membuat soal cerita pendek yang menarik berdasarkan ekspresi matematika yang diberikan. "
            "Gunakan bahasa Indonesia yang baku namun ramah anak. "
            "Hanya kembalikan teks soal ceritanya saja, jangan ada penjelasan tambahan."
        )
        
        user_prompt = (
            f"Buatlah soal cerita bertema '{theme}' untuk operasi berikut: {expression}. "
            f"Hasil akhirnya harus {result}. "
            f"Gunakan variabel yang masuk akal dalam tema tersebut."
        )

        try:
            async with httpx.AsyncClient(timeout=settings.LM_TIMEOUT_SECONDS) as client:
                response = await client.post(
                    self.api_url,
                    json={
                        "model": "local-model",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        "temperature": 0.7
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    story = data["choices"][0]["message"]["content"].strip()
                    return story
                else:
                    logger.warning(f"LM Studio returned status {response.status_code}")
        except Exception as e:
            logger.error(f"Failed to connect to LM Studio: {e}")

        # Fallback if AI fails
        return self._generate_fallback_story(expression, operation, theme, rng)

    def _generate_fallback_story(self, expression: str, operation: str, theme: str, rng: random.Random) -> str:
        """
        Fallback generator jika AI tidak tersedia.
        """
        # Objek-objek berdasarkan tema
        themes = {
            "buah-buahan": ["apel", "jeruk", "mangga", "pisang"],
            "luar angkasa": ["planet", "bintang", "astronot", "roket"],
            "sekolah": ["buku", "pensil", "penggaris", "tas"],
            "general": ["benda", "barang", "item", "objek"]
        }
        
        # Ambil list benda berdasarkan tema, fallback ke general jika tidak ada
        items = themes.get(theme.lower(), themes["general"])
        item = rng.choice(items)

        templates = {
            "addition": [
                "Budi memiliki {v1} {item}, lalu Susi memberinya {v2} {item} lagi. Berapa total {item} Budi?",
                "Di sebuah toko ada {v1} {item}, kemudian datang kiriman {v2} {item} baru. Berapa jumlah {item} sekarang?"
            ],
            "subtraction": [
                "Ibu membeli {v1} {item}, namun {v2} {item} hilang di jalan. Berapa sisa {item} Ibu?",
                "Ada {v1} {item} di meja, lalu {v2} {item} diambil oleh adik. Berapa {item} yang masih ada?"
            ],
            "multiplication": [
                "Ada {v1} kotak, masing-masing berisi {v2} {item}. Berapa total {item} seluruhnya?",
                "Seorang pedagang memiliki {v1} kantong {item}, tiap kantong ada {v2} {item}. Berapa total {item}?"
            ],
            "division": [
                "Ayah membagikan {v1} {item} kepada {v2} anaknya secara merata. Berapa {item} yang didapat tiap anak?",
                "Ada {v1} {item} yang akan dimasukkan ke dalam {v2} wadah sama banyak. Berapa isi tiap wadah?"
            ]
        }

        # Parsing operands from expression (very simple logic)
        try:
            # Handle standard expressions like "10 + 5" or "10 / 2"
            parts = expression.split()
            v1 = parts[0]
            v2 = parts[2]
            
            op_key = operation if operation in templates else "addition"
            template = rng.choice(templates.get(op_key, templates["addition"]))
            return template.format(v1=v1, v2=v2, item=item)
        except:
            return f"Hitunglah hasil dari {expression}."

ai_storyteller = AIStoryteller()
