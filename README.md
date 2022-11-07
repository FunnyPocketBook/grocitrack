## Known edge cases
- If there is a `B` at the end of an item, it means a bonus can be applied. This bonus shows up after the subtotaal. `aantal` is `bonus` and the description is the item name without spaces. `bedrag` is the bonus amount (negative number, e.g. `-0,50`)
- `Prijs` can have four digits, e.g. `30,00`. In that case, the last digit is moved to a newline, which is difficult to parse

Process:
- Parse the first element. Parsing must take only numbers or a number followed by `KG`, like `0.108KG`. If it is `KG`, that means there will also be a price per kg
- Parse the following elements until the next number is found. This is the description. Join the elements with a space
- Parse the next element. This is the price. In case of it being `KG`, the price is the price per kg and might be scuffed.

```
[['AANTAL', 'OMSCHRIJVING', 'PRIJS', 'BEDRAG'],
 ['', 'BONUSKAART', 'xx5571'],
 ['1', 'GORMAS', '70+', '2,79'],
 ['1', 'AH', 'SPINAZIE', '1,55'],
 ['2', 'SUBTOTAAL', '4,34']]

[['AANTAL', 'OMSCHRIJVING', 'PRIUS', 'BEDRAG'],
 ['', 'BONUSKAART', 'xxX5571'],
 ['1', 'AH', 'CREME', 'FR', '1,49'],
 ['1', 'HALFV', 'MELK', '1,69'],
 ['0.108KG', 'GRF', 'ROSBIEF', '30', '3,33'],
 ['1', 'AH', 'SPINAZIE', '1,55'],
 ['1', 'AH', 'RUCOLA', '1,00'],
 ['1', 'CHEDDAR', 'RASP', '2,49'],
 ['1', 'AH', 'KAAS', '2,49'],
 ['1', 'TOILETPAPIER', '6,99'],
 ['1', 'NALYS', 'KP', '10,79'],
 ['9', 'SUBTOTAAL', '31,82']]

[['AANTAL', 'OMSCHRIJVING', 'PRIJS', 'BEDRAG'],
 ['', 'BONUSKAART', 'xx5571'],
 ['1', 'GORMAS', '70+', '2,79'],
 ['1', 'AH', 'SPINAZIE', '1,55'],
 ['2', 'SUBTOTAAL', '4,34']]
 ```