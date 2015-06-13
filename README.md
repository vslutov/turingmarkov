# turingmarkov

Emulator of turing machine and markov algorithm.

## Нормальные алгоритмы Маркова

### Краткие теоретические сведения

Нормальный алгоритм Маркова (НАМ) -
один из стандартных способов формального определения понятия алгоритма
(другой известный способ — машина Тьюринга). Понятие нормального алгоритма
введено А. А. Марковым (младшим) в конце 1940-х годов в работах по
неразрешимости некоторых проблем теории ассоциативных вычислений.
Традиционное написание и произношение слова «алгорифм» в этом термине
также восходит к его автору, многие годы читавшему курс математической
логики на механико-математическом факультете МГУ.

Нормальный алгоритм описывает метод переписывания строк, похожий по способу
задания на формальные грамматики. НАМ является Тьюринг-полным языком,
что делает его по выразительной силе эквивалентным машине Тьюринга и,
следовательно, современным языкам программирования.
На основе НАМ был создан функциональный язык программирования Рефал.

### Описание

Нормальные алгоритмы являются вербальными, то есть предназначенными для
применения к словам в различных алфавитах.

Определение всякого нормального алгоритма состоит из двух частей:
определения алфавита алгоритма (к словам из символов которого алгорифм будет
применяться) и определения его схемы. Схемой нормального алгоритма называется
конечный упорядоченный набор так называемых формул подстановки,
каждая из которых может быть простой или заключительной.

1. Простыми формулами подстановки называются слова вида `L-> D`,
   где `L` и `D` — два произвольных слова в алфавите алгоритма (называемые,
   соответственно, левой и правой частями формулы подстановки).
2. Аналогично, заключительными формулами подстановки называются слова вида
   `L => D`, где `L` и `D` — два произвольных слова в алфавите алгоритма.

При этом предполагается, что вспомогательные буквы `->` и `=>` не принадлежат
алфавиту алгоритма (в противном случае на исполняемую ими роль разделителя
левой и правой частей следует избрать другие две буквы).

Процесс применения нормального алгоритма к произвольному слову `V` в алфавите
этого алгоритма представляет собой дискретную последовательность
элементарных шагов, состоящих в следующем.

Дана входная строка:

1. Проверить формулы в порядке следования  сверху вниз, присутствует ли левая
   часть формулы во входной строке.
2. Если такой формулы не найдено, алгоритм останавливается.
3. Если найдена одна или несколько формул, то самая верхняя из них
   используется для замены: самое левое вхождение левой части формулы во
   входной строке заменяется на правую часть формулы.
4. Если только что примененная формула была терминальной, то алгоритм
   останавливается.
5. Снова переходим к шагу 1.

Заметим, что после применения очередной формулы поиск следующей начинается
с самой верхней формулы.

### Примеры

#### Пример 1

В произвольном слове, состоящем из букв `{a, b, c}`, все подряд стоящие
одинаковые буквы заменить одной буквой (например, слово `abbbcaa`
преобразовать в `abca`). Схема НАМ. имеет вид:

    aa -> a
    bb -> b
    cc -> c

Применение этой схемы с слову `abbbcaa` последовательно даст слова:
`abbbca`, `abbca` и `abca`, после чего выполнение НАМ завершится.

#### Пример 2

Удвоить слово, состоящее из одинаковых символов (для определенности — `x`).
Т.е. слово `x` надо преобразовать в `xx`, слово `xx` — в `xxxx` и т.д.

Схема НАМ для этого примера намного сложнее, чем для примера 1.
Нельзя написать `x -> xx`, т.к. в этом случае на каждом шаге НАМ к слову будет
добавляться символ `x` и этот процесс будет бесконечным. Необходимо
контролировать удвоение каждого символа слова так, чтобы каждый символ
удвоился только один раз. Для это введём маркер, с помощью которого будем
обеспечивать контекст применения удваивающего правила.

    #x -> xx#
    #  =>
       -> #

Последнее правило вводит "маркер" `#` (или "курсор"), который с помощью
первого правила "перескакивает" через текущий символ слова и удваивает его.
Применение этой схемы, например, к слову "xx" последовательно даст слова
(в скобках указан номер применяемой формулы подстановки):

    (3) #xx
    (1) xx#x
    (1) xxxx#
    (2) xxxx

#### Пример 3

Дано слово в алфавите `{a, b, c}`. Упорядочить буквы входного слова в
лексикографическом порядке.

    ba -> ab
    ca -> ac
    cb -> bc

## References

1. <http://cmcmsu.no-ip.info/1course/alg.schema.nam.htm>
2. <https://ru.wikipedia.org/wiki/%D0%9D%D0%BE%D1%80%D0%BC%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9_%D0%B0%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC>
3. <https://en.wikipedia.org/wiki/Markov_algorithm>
