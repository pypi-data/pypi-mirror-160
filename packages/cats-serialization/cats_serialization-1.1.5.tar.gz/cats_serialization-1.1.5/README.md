Cats Serialization
==================
 
## Introduction
 
It is a simple, extensible and functional serializer for objects.
The goal of the project is to provide a developer with a simple tool for developing REST applications... and not only =)

More information in [wiki](http://git.vovikilelik.com/Clu/cats-serialization-10/wiki)

## Build

1. `python3 -m build`
2. `twine upload dist/*`

## Installation
`pip install cats-serialization`

## Main Features

* Multi style notation
* Serialization and deserialization
* Validation and logical operation with same
* Full-object validation possibility
* Union types supporting
* Correction values (by validators)

### Multi style notation
  
  ```python
  class Box(BaseSerializer):
    annotation: str
  
    field = Field()
    
    def virtual(self, data):
      return data.do_smth(), custom_name  # custom_name if needed

  ```


### Support for union operation

  ```python
    class Address(BaseSerializer):
        star: str
        planet: str
        moon: str | Undefined  # like not required
  
    class Box(BaseSerializer):
        address: str | Address  # can be string or object
    
    # It`s ok for:
    # { address: 'Sun, Mars' } 
    # { address: { star: 'Sun', planet: 'Mars' } }
  ```
  
  it works for fields notation
  
  ```python
    class Box(BaseSerialiser):
    
        # address is str or object
        address = Field(is_type=str) | ObjectField(Address)
  ```
  
### Logical operation with validators

  ```python
    one_field = Field(validator=IsType(int) | IsType(str))
    two_field = Field(validator=IsType(int) & IsRequired())
  ```

### Instance based serializer
 
  ```python
    class Box(Serialiser):
        pass
  
    box = Box()  # New instance
    print(box.serialize(data))
  ```

### Deserialization
  ```python
    class Goods:
        pass
  
    class Unpack(Deserializator):
        pass
  
    unpack = Unpack()
    goods = unpack.create(data, prototype=Goods)
  ```

### Correction values in passing
  ```python
    class IsName(BaseValidator):
        
        def validate(self, value, *args):
            if type(value) is not str:
                raise ValidationError('It is not the name')
            
            return value.strip()  # safe correction

    class Box(BaseSerializer):
        
        # name will be corrected if type check will be passed
        name = Field(validator=IsName())
  ```

## Uses

### Class-based scheme

If you need to create class based serializer, it will just inherit on `BaseSerializer` class

```python
class MyScheme(BaseSerializer):
    pass
```
Serialization
```python
# Call serialize(...) from class MyScheme instantly
some_dict = MyScheme.serialize(some_data)
```

### Instance-based serialisation
It helps if it really needed
```python
class MyScheme(Serializer):
    
    def __init__(self):
        pass
```
Serialization
```python
# At first, create instance
scheme = MyScheme()

# Now, you can call serialise(...)
some_dict = scheme.serialize(some_data)
```

### Common Fields

#### Annotations

If you uses annotations, all field will be had type-check validation

```python
class MyScheme(BaseSerializer):
    any: Any  # Any field
    
    string: str  # Primitive fields with type validation
    not_required: str | Undefined  # Not required field
    blank: str | None  # Can be blank field
    integer: int | str | bool  # Union fields

    list: list[str]  # Generic list
    
    item: ItemScheme  # Other serializer
    items: list[ItemScheme]  # List of other serializer
```

#### Fields
```python
class MyScheme(BaseSerializer):
    field = Field()  # Simple field
    
    item = ObjectField(ItemScheme)  # Other serializer
    items = IterableField(ItemScheme)  # List of other serializer
    
    required = Field(is_required=True)  # Any required field
    typed = Field(is_type=str)  # Required with type check
    
    # With validator
    validated = Field(validator=IsStrong() & IsRequired())
```

#### Methods
```python
class MyScheme(BaseSerializer):

    @classmethod
    def virtual(cls, data):
        return data.sub_field, 'override_name_if_needed'

    # it works, but be careful
    def virtual_self(self, data):
        return data.sub_field, 'override_name_if_needed'
```

### Base Fields inherit
```python
class MyField(BaseField):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
```

### Validation inherit

Generic validator has pattern:

```python
class MyValidator(BaseValidator):
    
    def validate(self, value, *args):
        if smth_wrong(value):
            raise ValidationError('Message')
```

You can make full-object validator. For example, it needs if one field will depend on another.

```python
class MyValidator(BaseValidator):
    
    def validate(self, value, key, data):  # use key and data
        if data.id == value:  # it`s just example
            raise ValidationError('Message')
```