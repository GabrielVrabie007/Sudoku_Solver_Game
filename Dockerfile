# 1. Folosește imaginea oficială Python slim
FROM python:3.11-slim

# 2. Instalează dependințele sistem necesare pentru Pygame
RUN apt-get update && apt-get install -y \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    libfreetype6 \
    libx11-6 \
    libxcursor1 \
    xorg \
    && rm -rf /var/lib/apt/lists/*

# 3. Setează directorul de lucru în container
WORKDIR /app

# 4. Copiază tot conținutul proiectului
COPY . .

# 5. Instalează Poetry și dependințele proiectului
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# 6. Setează variabile de mediu pentru Pygame
ENV SDL_VIDEODRIVER=x11

# 7. Schimbă în directorul sudoku
WORKDIR /app/sudoku

# 8. Setează punctul de intrare pentru scriptul principal
CMD ["python", "sudoku.py"]

