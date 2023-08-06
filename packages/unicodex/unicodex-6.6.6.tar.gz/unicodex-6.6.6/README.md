<div align="center">
<h1>Unicodex</h1>
Unicodes encoder, decoder & converter
</div>



<h2>Installation:</h2>

```bash
>>> python3 -m pip install unicodex
```

<h2>Examples:</h2>

```python
>>> from unicodex import Unicodex

>>> # Character to unicode
>>> c2u = Unicodex.chr(127914)

>>> # Unicode to character
>>> u2c = Unicodex.ord(c2u)

>>> # Encode text to unicode
>>> en = Unicodex.encode("Sample text", 666)

>>> # Decode unicode to text
>>> de = Unicodex.decode(en, 666)
```
