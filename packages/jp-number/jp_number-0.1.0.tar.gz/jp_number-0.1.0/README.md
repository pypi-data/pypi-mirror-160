# jp_numbers.
Convert numbers from/to Japanese Numbers
This is spin-off project from [jp_prefecture](https://pypi.org/project/jp-prefecture/)

## Install

`pip install jp_number`

## How to use

```python
from jp_number import JpNumberParser
jn = JpNumberParser()
```

## class JpNunberPaser

- `kanji2number(val)`
- `number2kanji(val, style)`
   - style: 'kanji', 'arabic', 'mix', 'finance', 'daiji'
- `normalize_kanjinumber(val)`

```python
In [1]: from jp_number import JpNumberParser

In [2]: jn = JpNumberParser()

In [3]: jn.number2kanji(87654)
Out[3]: JpNumber(number=87654, as_str='87654', as_kanji='八万七千六百五十四')

In [4]: jn.number2kanji(87654, style='arabic')
Out[4]: JpNumber(number=87654, as_str='87654', as_kanji='８７６５４')

In [5]: jn.number2kanji(87654, style='mix')
09:44:27.69 LOG:
09:44:27.78 .... count = 0
Out[5]: JpNumber(number=87654, as_str='87654', as_kanji='８万７６５４')

In [6]: jn.number2kanji(87654, style='finance')
Out[6]: JpNumber(number=87654, as_str='87654', as_kanji='８７，６５４')

In [7]: jn.number2kanji(87654, style='daiji')
Out[7]: JpNumber(number=87654, as_str='87654', as_kanji='捌萬漆仟陸佰伍拾肆')

In [8]: jn.kanji2number('八万七千六百五十四')
Out[8]: JpNumber(number=87654, as_str='87654', as_kanji='八万七千六百五十四')

In [9]: jn.kanji2number('８７６５４')
Out[9]: JpNumber(number=87654, as_str='87654', as_kanji='８７６５４')

In [10]: jn.kanji2number('８７，６５４')
Out[10]: JpNumber(number=87654, as_str='87654', as_kanji='８７，６５４')

In [11]: jn.kanji2number('捌萬漆仟陸佰伍拾肆')
Out[11]: JpNumber(number=87654, as_str='87654', as_kanji='捌萬漆仟陸佰伍拾肆')

In [12]: jn.kanji2number('天神四丁目')
Out[12]: JpNumber(number=4, as_str='4', as_kanji='天神四丁目')

In [13]: jn.kanji2number('天神４丁目')
Out[13]: JpNumber(number=4, as_str='4', as_kanji='天神４丁目')

In [14]: jn.normalize_kanjinumber('京都府長岡京市天神２丁目１５-１３')
Out[14]: '京都府長岡京市天神二丁目十五-十三'

```

