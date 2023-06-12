# Projekt GKOM - Chmury Punktów

## Struktura repozytorium

Kod źródłowy projektu znajduje się w folderze `src`. W folderze `assets` znajdują się przykładowe modele 3D, na których można przetestować projekt. W folderze `shaders` znajdują się pliki źródłowe shaderów.

Aby uruchomić program, należy po zainstalowaniu odpowiednich pakietów wykonać polecenie:

```
python .\src\main.py
```

Po chwili ukaże się okno wyświetlające domyślny model:

![Interfejs programu](.\images\viewport.png)

Można obracać kamerę wokół modelu poprzez przytrzymanie prawego przycisku myszy i przesuwanie kursora. Ruchy kursorem trzymając wciśnięty scroll powodują przesuwanie modelu, a ruchy scrolla powodują przybliżanie i oddalanie modelu.

## Rozwiązanie 

Projekt obejmuje program do wyświetlania modeli 3D opisanych jako chmury punktów. Możliwe jest utworzenie dowolnej liczby modeli do wyświetlania poprzez dodanie ich do listy `objects` która jest parametrem wywołania funkcji `main` w pliku `.\src\main.py`. Modele są niezależnymi instancjami klasy `Object`, która przechowuje informacje o pozycji, skali, kolorze i shaderze danego modelu. Same modele renderowane są poprzez wyświetlanie utworzonych za pomocą geometry shaderów splatów w miejscach występowania punktów. Zaimplementowaliśmy także algorytm który poprzez obliczenie odległości danego punktu do najbliżeszego sąsiadującego mu punktu w modelu automatycznie skaluje rozmiar splatów, aby w miarę równomiernie pokryć całą powierzchnię modelu. Dzięki temu uzyskujemy efekt wyświetlania modelu jako chmury punktów, a nie jako pojedynczych punktów.

## Materiały dodatkowe

Aby lepiej wyjaśnić działanie systemu dynamicznego skalowania splatów, utworzyliśmy dwa przykładowe skrypty wyświetlające kilka rozrzuconych po ekranie punktów. Do skalowania jednego z nich (`.\examples\resize_splats_uniform.py`, po lewej) używamy skalowania równomiernego, natomiast w drugim przypadku (`.\examples\resize_splats_log.py`, po prawej) używamy skalowania logarytmicznego. Porównanie obu metod przedstawia poniższy obraz:

![Porównanie metod skalowania](.\images\resizing_comp.png)

W repozytorium znajduje się również kilka innych skryptów przykładowych na których wzorowaliśmy się podczas tworzenia kompletnego rozwiązania.
