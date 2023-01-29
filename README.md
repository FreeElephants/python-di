# fe-python-di

Simple python dependency injection implementation.

```bash
pip install fe-python-di
```

```python
from di import DI

di = DI()

# set preconfigured component to container
di[InjectedService] = InjectedService()

# get instance by type name
some_service: SomeYourComponentName = di.get(SomeYourComponentName)
```


