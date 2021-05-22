# cryptocurrencies_app

Crypto Analyser v.1

Aplikacja web umożliwiająca podgląd i analizę danych o kryptowalutach. Aplikacja korzysta z publicznego API serwisu BitBay.

API dostępne pod adresem: https://docs.bitbay.net/reference

Na potrzeby analizy danych wykorzystane zostały wykresy świec (kursy otwarcia, zamknięcia, wolumen) oraz bieżące kursy walut dostępne pod adresem /stats/.

Aplikacja składa się z:
    - strony głównej
    - listy kryptowalut dostępnych w serwisie BitBay 
    - danych historycznych dla każdej waluty (wykres, dane tabelaryczne) 
    - analizy danych (predykcja wykorzystująca model LSTM - Long Short Term Memory) 

Do wykonania predykcji wykorzystana została sieć neuronowa RNN-LTSM.
LSTM jako long short term memory) to architektura rekurencyjnej sieci neuronowej, która w procesie nauki zapamiętuje wartości w dowolnych przedziałach. Tego typu 
architektura jest odpowiednia do klasyfikowania, przetwarzania i prognozowania szeregów czasowych, w których pomiędzy ważnymi zdarzeniami występują przesunięcia 
czasowe nieznanych rozmiarów i długości.

Niezbędne biblioteki: 
    - Keras / Tensorflow (w celu budowy modelu sieci neuronowej) 
    - matplotlib, pandas, numpy (biblioteki matematyczne do tworzenia macierzy i list) 
    - BytesIO, base64 (do konwersji wykresów)

Aplikacja może zostać rozbudowana o kolejne funkcjonalności. 

Przyszłe cele: stworzenie panelu logowania dla każdego użytkownika, umożliwienie exportu danych do pliku .csv, maksymalizacja dopasowania modelu predykcji, aktualizacja szaty graficznej.

Aplikacja napisana w Django v. 3.1.7.
Autor: Mjnrt