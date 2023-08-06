# 1DECA
generate one dimensional elementary cellular automata


## Install
`pip install eca`

## Example

```python
from eca import OneDimensionalElementaryCellularAutomata

configuration = OneDimensionalElementaryCellularAutomata(initial_configuration="0000100001011")

for _ in range(100):
    configuration.transition(rule_number=110)

print(str(configuration))
imshow(configuration.evolution())
```

## More Examples

see `example.ipynb`
