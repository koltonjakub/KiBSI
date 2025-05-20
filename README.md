# Repozytorium dla projektu zaliczeniowego z przedmiotu Kryptografia i Bezpieczeństwo Systemów Informatycznych
Autor: Jakub Kołton
Kierunek: Automatyka i Robotyka: Inteligentne Systemy Sterowania
Wydział: Elektrotechniki Automatyki Informatyki i Inżynierii Biomedycznej
Data: 27 Maj 2025r.

# Wymagania systemowe
- python >= 3.10
- pyqt = 5.15.10
- qiskit = 1.4.2
- qiskit-aer = 0.17
- zalecane użycie wirtualnego środowiska do języka Python (venv, conda etc.)

# Opis projektu
Aplikacja pozwala na zaprezentowanie działania algorytmu kwantowej wymiany klucza BB84 z uwzględnionym podsłuchem[1].
W polach RND Key length oraz Eavesdropping % należy wpisać odpowiednio długość losowego klucza (liczba naturalna dodatnia) oraz średni procent kubitów jaki zostanie poddany podsłuchowi (libcza rzeczywista w zakresie od 0 do 100). Po kliknięciu start algorytm się wykona, a w polach poniżej pokażą się odpowiednie ciągi bitów:
1. Alice: Losowy klucz wygenerowany przez Alicję
2. Bazy(Alice): Losowe bazy Alicji
3. Bazy(Bob): Losowe bazy Boba
4. Bob: Ciąg bitów uzyskany przez Boba po wykonaniu pomiarów
5. Eve: Stosunek bitów różniących się w kluczu Alicji i Boba do bitów podsłuchanych.

Na niebiesko zaznaczono bity kluczy A. i B. których odpowiadające im bazy są takie same, tylko te bity są brane pod uwagę jako fragment klucza.

# Uruchomienie
w celu uruchomienia aplikacji należy wywołać komendę
python3 __main__.pyw
w terminalu z głównego folderu projektu. W konsoli będą się pojawiać ew. komunikaty o błędach wykonania.

# Źródła
1. "28.Quantum key distribution I: BB84 protocol", Jochen Rau, https://www.youtube.com/watch?v=u_K9jPBrOwA dostęp: 20 maj 2025r.