<h1 align="center">🔗 OpenIP</h1>

<div align="center">
Zaawansowane narzędzie do analizy i testowania sieci prywatnych.<br>
Projekt edukacyjny (EDU).
</div>

---

<h2 align="center">⚠️ Uwaga</h2>

<strong>Używaj wyłącznie na sieciach, które posiadasz lub na które masz wyraźną zgodę.</strong>

Nieautoryzowane skanowanie sieci może być nielegalne i prowadzić do konsekwencji prawnych.  
Autor nie ponosi odpowiedzialności za niewłaściwe użycie narzędzia.

---

<h2 align="center">📋 Spis treści</h2>

- [O projekcie](#-o-projekcie)
- [Wymagania](#-wymagania)
- [Instalacja](#-instalacja)
- [Użycie](#-użycie)
- [Funkcje](#-funkcje)
- [Licencja](#-licencja)

---

<h2 align="center">📖 O projekcie</h2>

**OpenIP** to narzędzie do diagnostyki i analizy sieci prywatnych.  
Pozwala na wykrywanie aktywnych hostów, skanowanie portów oraz podstawowe
rozpoznawanie usług działających w sieci.

Projekt ma charakter **edukacyjny** i służy do nauki bezpieczeństwa sieci
w kontrolowanym środowisku.

---

<h2 align="center">🔧 Wymagania</h2>

- **Python 3.8+**
- Windows / Linux / macOS
- (Opcjonalnie) uprawnienia administratora

---

<h2 align="center">📥 Instalacja</h2>

### 1️⃣ Instalacja Pythona

Pobierz Python z oficjalnej strony:  
👉 https://www.python.org/downloads/

Podczas instalacji zaznacz opcję **Add Python to PATH**.

### 2. Weryfikacja instalacji

Sprawdź, czy Python został poprawnie zainstalowany:

```bash
python --version
```

### 3. Klonowanie repozytorium

Kliknij zielony przycisk code oraz znajdź na dole okienka przycisk **"Download .zip"**
Wypakuj plik .zip do folderu download na Windows/Linux i przenieś plik OPEN-IP.py do katalogu domowego "C://User/user"

<h2 align="center">🚀 Użycie</h2>

### Uruchomienie w terminalu

```bash
python OPEN-IP.py
```

### Przykładowe komendy

```bash
# Pomoc
help

# Skanowanie portów
scan

# Pełne skanowanie portów (Trwa kilka minut)
scan full

# Skanowanie topowych portów
skan fast

# Sprawdzanie konkretnego IP
ping

# Skan sieci ip.1-24
net

# Informacje o sieci
info
```

### PrintScreen
*Uwaga niektóre zrzuty ekranu są w wersji demo dla prywatności twórcy*

![help](./img/help.png)
![info](./img/info.png)
![ping](./img/ping.png)
![scan](./img/scan/basic.png)
![scanfull](./img/scan/full.png)
![scanfast](./img/scan/fast.png)
![net](./img/net.png)

---

<h2 align="center">✨ Funkcje</h2>

- 🔍 **Skanowanie sieci** - Wykrywanie aktywnych hostów w sieci
- 🔐 **Analiza portów** - Identyfikacja otwartych portów i usług
- ⚡ **Szybkie skanowanie** - Zoptymalizowane algorytmy

---

<h2 align="center">📄 Licencja</h2>

Ten projekt jest udostępniony bez licencji.

---

<div align="center">
   <p>Stworzone z ❤️ przez Enlvis</p>
   <p>⭐ Jeśli podoba Ci się projekt, zostaw gwiazdkę na GitHubie! ⭐</p>
</div>

