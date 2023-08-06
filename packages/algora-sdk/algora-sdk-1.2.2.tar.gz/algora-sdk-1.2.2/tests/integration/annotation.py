import json
import unittest

from algoralabs.common.base import Base, create_annotation
from typing_extensions import Literal

from algoralabs.decorators.serializable import serializable


class Parent(Base):
    x: int
    y: int


@serializable
class Foo(Parent):
    pass


@serializable
class Bar(Parent):
    pass


@serializable
class Fizz(Parent):
    pass


AnnotatedClass = create_annotation(Foo, Bar)


class Container(Base):
    foo: AnnotatedClass.annotation()
    bar: AnnotatedClass.annotation()
    generic: AnnotatedClass.annotation()

    @classmethod
    def new_fields(cls):
        return {field: (AnnotatedClass.annotation(), None) for field in ['foo', 'bar', 'generic']}


class ContainerSquared(Base):
    container: Container

    @classmethod
    def new_fields(cls, updated_container_cls):
        return {'container': (updated_container_cls, None)}


class TestAnnotatedSerialization(unittest.TestCase):
    def setUp(self) -> None:
        self.foo = Foo(x=0, y=0)
        self.bar = Bar(x=1, y=1)
        self.fizz = Fizz(x=2, y=2)

    def assert_serialization(self, obj, cls):
        serialized_data = json.loads(obj.json())
        deserialized_data = cls(**serialized_data)
        self.assertEqual(obj, deserialized_data)

    def test_defined_annotation(self):
        container = Container(foo=self.foo, bar=self.bar, generic=self.foo)
        container_squared = ContainerSquared(container=container)

        self.assert_serialization(container, Container)
        self.assert_serialization(container_squared, ContainerSquared)

    def test_updated_annotation(self):
        AnnotatedClass.add_types(Fizz)
        C = Container.update()
        CSquared = ContainerSquared.update(C)

        container = C(foo=self.foo, bar=self.bar, generic=self.fizz)
        container_squared = CSquared(container=container)

        self.assert_serialization(container, C)
        self.assert_serialization(container_squared, CSquared)
