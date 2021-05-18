# cryptocurrencies_app

Crypto Analyser v.1

Aplikacja web umożliwiająca podgląd i analizę danych o kryptowalutach. Aplikacja korzysta z publicznego API serwisu BitBay.

API dostępne pod adresem: https://docs.bitbay.net/reference

Na potrzeby analizy danych wykorzystane zostały wykresy świec (kursy otwarcia, zamknięcia, wolumen) oraz bieżące kursy walut dostępne pod adresem /stats/.

Aplikacja składa się z:
    - strony głównej
    - listy kryptowalut dostępnych w serwisie BitBay
    - danych historycznych dla każdej waluty (wykres, dane tabelaryczne)
    - analizy danych (predykcja wykorzystująca model LSTM - Long Short Time Memory)

Aplikacja napisana w Django v. 3.1.7.
Autor: Mjnrt
