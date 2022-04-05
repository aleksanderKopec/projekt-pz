# Programowanie Zespołowe: Projekt

## Zamysł projektu

Stworzenie publicznego czatu internetowego pozwalającego na dołączenie do danego kanału podając nazwę użytkownika oraz identyfikator pokoju będący dowolnym ciągiem znaków.
Ma to na celu zachęcenie użytkownika do 'eksplorowania' pokoi czatowych, poznawanie innych użytkowników oraz przyczyniać się do charakteru 'tajemniczości' korzystania z aplikacji.

### Przykładowe scenariusze:

- Użytkownik podaje 'star wars' jako identyfikator pokoju. Po połączeniu okazuje się że w czacie trwa właśnie dyskusja fanów Gwiezdnych Wojen na temat najnowszego filmu.
- Użytkownik podaje 'abcd' jako identyfikator pokoju. Kanał do tego czasu był nieaktywny i został właśnie utworzony przez użytkownika. Może on zostawić wiadomość dla kogoś, kto być może kiedyś również wprowadzi ten identyfikator.
- Użytkownik wkleja cały tekst wiersza Juliana Tuwima "Lokomotywa" do pola tekstowego. Odkrywa, że kilku innych użytkowników wpadło już wcześniej na ten pomysł i zostawili wiadomości na na tym kanale.

### Zabezpieczenie przed automatycznym przeszukiwaniem kanałów

W celu zapobiegnięciu zautomatyzowanemu przeszukiwaniu aktywnych kanałów zostaną wprowadzone mechanizmy wprowadzające opóźnienie w dołączeniu do każdego kolejnego kanału użytkownika.
