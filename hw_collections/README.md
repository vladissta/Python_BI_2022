Скрипт работает с последовательностями нуклеотидов (РНК и ДНК)

При запуске скрипт предложит ввести команду, взавсисимости от того, какую операцию хочет пользователь произветси над последовательностью. 
При этом скрипт напишет список доступных команд.  
Если команда была введена некорректно, то скрипт попросит пользователя ввести ее еще раз.

_Список доступных команд:_  
**exit** — завершение исполнения программы  
**transcribe** — напечатать транскрибированную последовательность  
**reverse** — напечатать перевёрнутую последовательность  
**complement** — напечатать комплементарную последовательность. Если будет введена последовательность _РНК_, то скрипт выведет комплементарную ей последовательность _РНК_. Аналогично с  последовательностями ДНК.   
**reverse complement** — напечатать обратную комплементарную последовательность  

Далее скрипт попросит ввести последовательность, над которой будет проивзводиться данная команда.  

При этом _скрипт попросит написать последовательность еще раз_:  
1) Если будет введена не нуклеодитная последовательность.
2) Если будет введена нуклеотидная последовательность, где присутствуют и U, и T.
3) Если будет введена команда **transcribe**, а затем будет введена последовательность РНК.

При успешном выполнении команды скрипт выведет результат, который эта команда подразумевала (см. _Список доступных команд_) и предложит ввести новую команду.  

Скрипт завершает свою работу _только при вводе команды_ **exit**